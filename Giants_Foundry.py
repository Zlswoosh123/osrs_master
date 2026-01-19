import win32gui
import core
import yaml
from functions import (Image_count, invent_enabled,
                       move_mouse, click_object, screen_Image, Image_to_Text, resizeImage)
from PIL import ImageGrab, Image
import os, re
import numpy as np
import cv2
import time
import random
import pyautogui
import pytesseract
global hwnd
global iflag
global icoord
iflag = False

DEBUG = True  # flip False to quiet logs

def log(msg: str):
    """Timestamped log line."""
    if not DEBUG:
        return
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

def fmt_xy(info: dict) -> str:
    x = info.get("click_x")
    y = info.get("click_y")
    area = info.get("area")
    return f"x={x} y={y} area={area}"


def debug_color_snapshot(region, target_bgr, tol=50, path_prefix="dbg_deposit"):
    img_bgr, (L, T) = grab_client_region(region)
    B,G,R = target_bgr
    lower = np.array([clamp255(B - tol), clamp255(G - tol), clamp255(R - tol)], np.uint8)
    upper = np.array([clamp255(B + tol), clamp255(G + tol), clamp255(R + tol)], np.uint8)
    mask = cv2.inRange(img_bgr, lower, upper)
    cv2.imwrite(f"{path_prefix}_region.png", img_bgr)
    cv2.imwrite(f"{path_prefix}_mask.png", mask)
    # print(f"[debug] wrote {path_prefix}_region.png and {path_prefix}_mask.png")

def gfindWindow(data):  # find window name returns PID of the window
    global hwnd
    hwnd = win32gui.FindWindow(None, data)
    # hwnd = win32gui.GetForegroundWindow()860
    #print('findWindow:', hwnd)
    win32gui.SetActiveWindow(hwnd)
    # win32gui.ShowWindow(hwnd)
    win32gui.MoveWindow(hwnd, 0, 0, 865, 830, True) #(hwnd, 0, 0, 865, 830, True)


with open("pybot-config.yaml", "r") as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)

try:
    gfindWindow(data[0]['Config']['client_title'])
except BaseException:
    print("Unable to find window:", data[0]['Config']['client_title'], "| Please see list of window names below:")
    core.printWindows()
    pass

try:
    x_win, y_win, w_win, h_win = core.getWindow(data[0]['Config']['client_title'])
except BaseException:
    print("Unable to find window:", data[0]['Config']['client_title'], "| Please see list of window names below:")
    core.printWindows()
    pass

def ensure_client_foreground():
    """Bring the client window to the front (best-effort; safe if it fails)."""
    try:
        window = win32gui.FindWindow(None, data[0]['Config']['client_title'])
        win32gui.ShowWindow(window, 5)
        win32gui.SetForegroundWindow(window)
        win32gui.SetActiveWindow(window)
    except Exception:
        pass

INVENT_CAPACITY = 28
INV_LEFT, INV_TOP, INV_RIGHT, INV_BOTTOM = 620, 460, 812, 735

def click_client(x, y, jitter=0, move_dur=(0.12, 0.25)):
    x0, y0 = get_client_origin()
    tx = x0 + x + random.randint(-jitter, jitter)
    ty = y0 + y + random.randint(-jitter, jitter)
    pyautogui.moveTo(tx, ty, duration=random.uniform(*move_dur))
    pyautogui.click()

def get_client_origin():
    """
    Return (x0, y0) top-left of client window, always without raising NameError.
    Caches into x_win/y_win/w_win/h_win globals when we discover them.
    """
    global x_win, y_win, w_win, h_win
    x0 = globals().get('x_win', 0)
    y0 = globals().get('y_win', 0)
    if x0 == 0 and y0 == 0:
        # Try core.getWindow first
        try:
            x_win, y_win, w_win, h_win = core.getWindow(data[0]['Config']['client_title'])
            x0, y0 = x_win, y_win
        except Exception:
            # Win32 fallback
            try:
                hwnd_local = win32gui.FindWindow(None, data[0]['Config']['client_title'])
                l, t, r, b = win32gui.GetWindowRect(hwnd_local)
                x_win, y_win, w_win, h_win = l, t, r - l, b - t
                x0, y0 = x_win, y_win
            except Exception:
                # Leave (0,0); caller may warn if window isn't pinned there
                x0, y0 = 0, 0
    return x0, y0


def grab_client_region(region=None):
    x0, y0 = get_client_origin()
    ww = globals().get('w_win', 0)
    hh = globals().get('h_win', 0)

    if region is None:
        left, top = x0, y0
        right  = x0 + (ww or 865)   # fallback to your MoveWindow width if you pin it
        bottom = y0 + (hh or 830)
    else:
        l, t, r, b = region
        left, top, right, bottom = x0 + l, y0 + t, x0 + r, y0 + b

    im = ImageGrab.grab(bbox=(left, top, right, bottom))
    bgr = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
    return bgr, (left, top)



def clamp255(x):
    return max(0, min(255, int(x)))

def click_color_bgr_in_region(
    target_bgr=(255,173,0),          # teal in BGR (FF00ADFF -> ARGB -> BGR)
    tol=45,                           # per-channel tolerance (try 45–60 while tuning)
    region=None,                      # [l,t,r,b] client-relative (None = whole client)
    min_area=30,                      # accept small blobs; we'll still click centroid fallback
    max_tries=3,
    morph_kernel=3,
    post_click_sleep=(0.45, 0.9),
    debug=False,
    use_hsv=True                     # set True if BGR path is flaky
):
    """
    Find a blob of the target color in the region and click its centroid.
    Returns (ok: bool, info: dict). Writes dbg images when debug=True.
    """
    ensure_client_foreground()
    last_info = {}
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (morph_kernel, morph_kernel))


    for attempt in range(max_tries):
        img_bgr, _ = grab_client_region(region)

        if use_hsv:
            # --- HSV masking (more robust to AA/lighting) ---
            tgt = np.uint8([[list(target_bgr)]])
            tH, tS, tV = cv2.cvtColor(tgt, cv2.COLOR_BGR2HSV)[0, 0]
            tH, tS, tV = int(tH), int(tS), int(tV)  # avoid uint8 overflow
            h_tol = 10
            s_tol = max(50, tol)
            v_tol = max(50, tol)
            h_lo, h_hi = tH - h_tol, tH + h_tol
            s_lo, s_hi = max(0, tS - s_tol), min(255, tS + s_tol)
            v_lo, v_hi = max(0, tV - v_tol), min(255, tV + v_tol)

            img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
            if h_lo < 0:
                lo1 = np.array([0,   s_lo, v_lo], np.uint8)
                hi1 = np.array([min(179, h_hi), s_hi, v_hi], np.uint8)
                lo2 = np.array([179 + h_lo, s_lo, v_lo], np.uint8)
                hi2 = np.array([179,        s_hi, v_hi], np.uint8)
                mask = cv2.bitwise_or(cv2.inRange(img_hsv, lo1, hi1),
                                      cv2.inRange(img_hsv, lo2, hi2))
            elif h_hi > 179:
                lo1 = np.array([max(0, h_lo), s_lo, v_lo], np.uint8)
                hi1 = np.array([179,          s_hi, v_hi], np.uint8)
                lo2 = np.array([0,            s_lo, v_lo], np.uint8)
                hi2 = np.array([h_hi - 179,   s_hi, v_hi], np.uint8)
                mask = cv2.bitwise_or(cv2.inRange(img_hsv, lo1, hi1),
                                      cv2.inRange(img_hsv, lo2, hi2))
            else:
                lo = np.array([h_lo, s_lo, v_lo], np.uint8)
                hi = np.array([h_hi, s_hi, v_hi], np.uint8)
                mask = cv2.inRange(img_hsv, lo, hi)
        else:
            # --- Original BGR masking ---
            B, G, R = target_bgr
            lower = np.array([clamp255(B - tol), clamp255(G - tol), clamp255(R - tol)], np.uint8)
            upper = np.array([clamp255(B + tol), clamp255(G + tol), clamp255(R + tol)], np.uint8)
            mask = cv2.inRange(img_bgr, lower, upper)

        # Thicken/close holes so thin outlines become solid blobs
        if morph_kernel > 1:
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k, iterations=2)
            mask = cv2.dilate(mask, k, iterations=1)

        cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not cnts:
            # ---- Fallback: centroid of all non-zero pixels ----
            nz = cv2.findNonZero(mask)
            if nz is not None and len(nz) > 0:
                cx = int(np.mean(nz[:, 0, 0]))
                cy = int(np.mean(nz[:, 0, 1]))
                rel_x = cx + (0 if region is None else region[0])
                rel_y = cy + (0 if region is None else region[1])
                if debug:
                    cv2.imwrite("dbg_deposit_region.png", img_bgr)
                    cv2.imwrite("dbg_deposit_mask.png", mask)
                    print(f"[color] attempt {attempt+1}: no contours; using nonzero centroid @{rel_x},{rel_y}")
                click_client(rel_x, rel_y, jitter=0)
                time.sleep(random.uniform(*post_click_sleep))
                return True, {
                    "attempt": attempt + 1,
                    "area": 0.0,
                    "found": 0,
                    "fallback": "nonzero-centroid",
                    "click_x": rel_x,
                    "click_y": rel_y
                }
            # else truly nothing detected
            last_info = {"attempt": attempt+1, "area": 0.0, "found": 0}
            if debug:
                cv2.imwrite("dbg_deposit_region.png", img_bgr)
                cv2.imwrite("dbg_deposit_mask.png", mask)
                print(f"[color] attempt {attempt+1}: empty mask; wrote dbg images")
            time.sleep(random.uniform(0.15, 0.30))
            continue

        # Largest contour
        c = max(cnts, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        last_info["bbox"] = (x, y, w, h)
        area = float(cv2.contourArea(c))
        last_info = {"attempt": attempt+1, "area": area, "found": len(cnts)}

        # Compute click point (moments with robust fallback)
        if area < float(min_area):
            nz = cv2.findNonZero(mask)
            if nz is None or len(nz) == 0:
                if debug:
                    print(f"[color] attempt {attempt+1}: small area={area:.1f}, no nonzero; retrying…")
                time.sleep(random.uniform(0.15, 0.30))
                continue
            cx = int(np.mean(nz[:, 0, 0]))
            cy = int(np.mean(nz[:, 0, 1]))
        else:
            M = cv2.moments(c)
            if M["m00"] == 0:
                x, y, w, h = cv2.boundingRect(c)
                cx = x + w // 2
                cy = y + h // 2
            else:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])

        rel_x = cx + (0 if region is None else region[0])
        rel_y = cy + (0 if region is None else region[1])

        if debug:
            print(f"[color] click @ client-rel [{rel_x}, {rel_y}] area={area:.1f} found={len(cnts)}")

        click_client(rel_x, rel_y, jitter=0)
        time.sleep(random.uniform(*post_click_sleep))

        last_info["click_x"] = rel_x
        last_info["click_y"] = rel_y

        return True, last_info

    return False, last_info

def _color_present_in_region(
    target_bgr,
    tol,
    region,
    use_hsv=True,
    morph_kernel=3,
    min_pixels=60
) -> bool:
    """
    Simple 'is this color present here?' check.
    Returns True if enough pixels match the mask.
    """
    img_bgr, _ = grab_client_region(region)

    if use_hsv:
        tgt = np.uint8([[list(target_bgr)]])
        tH, tS, tV = cv2.cvtColor(tgt, cv2.COLOR_BGR2HSV)[0, 0]
        tH, tS, tV = int(tH), int(tS), int(tV)

        h_tol = 10
        s_tol = max(50, tol)
        v_tol = max(50, tol)

        img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

        h_lo, h_hi = tH - h_tol, tH + h_tol
        s_lo, s_hi = max(0, tS - s_tol), min(255, tS + s_tol)
        v_lo, v_hi = max(0, tV - v_tol), min(255, tV + v_tol)

        if h_lo < 0:
            lo1 = np.array([0, s_lo, v_lo], np.uint8)
            hi1 = np.array([min(179, h_hi), s_hi, v_hi], np.uint8)
            lo2 = np.array([179 + h_lo, s_lo, v_lo], np.uint8)
            hi2 = np.array([179, s_hi, v_hi], np.uint8)
            mask = cv2.bitwise_or(cv2.inRange(img_hsv, lo1, hi1),
                                  cv2.inRange(img_hsv, lo2, hi2))
        elif h_hi > 179:
            lo1 = np.array([max(0, h_lo), s_lo, v_lo], np.uint8)
            hi1 = np.array([179, s_hi, v_hi], np.uint8)
            lo2 = np.array([0, s_lo, v_lo], np.uint8)
            hi2 = np.array([h_hi - 179, s_hi, v_hi], np.uint8)
            mask = cv2.bitwise_or(cv2.inRange(img_hsv, lo1, hi1),
                                  cv2.inRange(img_hsv, lo2, hi2))
        else:
            lo = np.array([h_lo, s_lo, v_lo], np.uint8)
            hi = np.array([h_hi, s_hi, v_hi], np.uint8)
            mask = cv2.inRange(img_hsv, lo, hi)
    else:
        B, G, R = target_bgr
        lower = np.array([clamp255(B - tol), clamp255(G - tol), clamp255(R - tol)], np.uint8)
        upper = np.array([clamp255(B + tol), clamp255(G + tol), clamp255(R + tol)], np.uint8)
        mask = cv2.inRange(img_bgr, lower, upper)

    if morph_kernel and morph_kernel > 1:
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (morph_kernel, morph_kernel))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k, iterations=1)

    matched = int(cv2.countNonZero(mask))
    return matched >= int(min_pixels)

def wait_for_expected_arrow(stage: str, timeout=7.0, poll_sleep=0.10) -> bool:
    """
    After a pink click, wait until the expected arrow appears based on stage.
    Returns True if arrow found, False if timed out (failsafe).
    """
    start = time.time()

    if stage == "polish":
        check_fn = bar_check_green
        check_name = "GREEN"
    elif stage == "grind":
        check_fn = bar_check_yellow
        check_name = "YELLOW"
    else:
        check_fn = bar_check_red
        check_name = "RED"

    log(f"[arrow-wait] stage={stage} waiting for {check_name} arrow (timeout={timeout}s)")

    last_report = 0.0
    while (time.time() - start) < timeout:
        n = check_fn()  # treat >=1 as true
        if n >= 1:
            log(f"[arrow-wait] found {check_name} arrow (count={n}) after {time.time()-start:.2f}s")
            move_mouse(650, 665, 500, 515)  # move to first obj in inv (next box)
            random_wait(.05, .2)
            click_object()
            random_wait(.05, .2)
            return True

        # occasional heartbeat so you know it's alive (every ~2s)
        elapsed = time.time() - start
        if elapsed - last_report >= 2.0:
            log(f"[arrow-wait] still waiting... {elapsed:.1f}s")
            last_report = elapsed

        time.sleep(poll_sleep)

    log(f"[arrow-wait] TIMEOUT after {timeout}s (failsafe resume)")
    return False



def wait_until_color_gone(
    target_bgr,
    tol,
    click_x,
    click_y,
    halfsize=50,
    timeout=0.01,
    poll_sleep=0.02,
    use_hsv=True,
    morph_kernel=3,
    min_pixels=60,
    clamp_bounds=None   # <-- NEW: (L,T,R,B) bounds to clamp ROI
) -> bool:
    start = time.time()

    if clamp_bounds is None:
        clamp_bounds = (0, 0, 865, 830)  # old behavior

    bound_L, bound_T, bound_R, bound_B = clamp_bounds

    L = max(bound_L, int(click_x - halfsize))
    T = max(bound_T, int(click_y - halfsize))
    R = min(bound_R, int(click_x + halfsize))
    B = min(bound_B, int(click_y + halfsize))

    region = [L, T, R, B]

    while (time.time() - start) < timeout:
        if not _color_present_in_region(
            target_bgr=target_bgr,
            tol=tol,
            region=region,
            use_hsv=use_hsv,
            morph_kernel=morph_kernel,
            min_pixels=min_pixels
        ):
            return True
        time.sleep(poll_sleep)

    return False

def strip_nums_parens_percent(text: str) -> str:
    # remove digits, parentheses, and percent sign
    text = re.sub(r'[\d()%]', '', text)
    # normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def inv_count(name):
    return Image_count(name + '.png', threshold=0.8, left=0, top=0, right=810, bottom=750)

def icon_check(name='empty_all_icon'):
    return Image_count(name + '.png','bank_image', threshold=0.7, left=388, top=603, right=552, bottom=648)

def bar_check_all(name='gf_arrow_green'):
    return Image_count(name + '.png','gf_bar.enhanced', threshold=0.8, left=99, top=80, right=539, bottom=105)

def bar_check_green(name='gf_arrow_green'):
    return Image_count(name + '.png','gf_bar_green', threshold=0.8, left=165, top=80, right=222, bottom=105)

def bar_check_yellow(name='gf_arrow_yellow'):
    return Image_count(name + '.png','gf_bar_yellow', threshold=0.8, left=265, top=80, right=330, bottom=105)

def bar_check_red(name='gf_arrow_red'):
    return Image_count(name + '.png','gf_bar_red', threshold=0.8, left=460, top=80, right=520, bottom=105)

def random_wait(a=.1, b=.3):
    c = random.uniform(a, b)
    time.sleep(c)

def stage_check():
    screen_Image(60, 767, 143, 786, 'gf_stage.png')
    stage = Image_to_Text('thresh', 'gf_stage.png')
    stage_stripped = strip_nums_parens_percent(stage).lower()
    grind_words = ['grind']
    polish_words = ['polish']
    print('Stage_stripped is:', stage_stripped)
    if stage_stripped in grind_words:
        stage_final = 'grind'
        return stage_final
    if stage_stripped in polish_words:
        stage_final = 'polish'
        return stage_final
    else:
        stage_final = 'hammer'
        return stage_final




time_left = 0
#-------------------------------

if __name__ == "__main__":
    Run_Duration_hours = 0.5
    t_end = time.time() + (60 * 60 * Run_Duration_hours)

    SEARCH_REGION = [0, 130, 600, 700]
    ACTIVE_BOUNDS = (SEARCH_REGION[0], SEARCH_REGION[1], SEARCH_REGION[2], SEARCH_REGION[3])

    # --- Per-color wait tuning (THIS is how you control wait times) ---
    # timeout = max time to wait for the clicked color to disappear
    # poll_sleep = how often we check (lower = faster CPU + faster reaction)
    # halfsize = ROI size around click (smaller = less noise)
    WAIT_BLUE  = dict(timeout=0.45, poll_sleep=0.015, halfsize=50, min_pixels=60)
    WAIT_PINK  = dict(timeout=0.60, poll_sleep=0.020, halfsize=50, min_pixels=60)
    WAIT_GREEN = dict(timeout=0.01, poll_sleep=0.005, halfsize=50, min_pixels=60)

    # Colors (B, G, R)
    BLUE_BGR  = (255, 0, 0)
    PINK_BGR  = (240, 0, 255)
    GREEN_BGR = (0, 255, 0)
    PURPLE_BGR = (65, 4, 41)

    while time.time() < t_end:
        last_stage = None
        stage=stage_check()
        if stage != last_stage:
            count = bar_check_green()
            count2 = bar_check_yellow()
            count3 = bar_check_red()
            log(f"[stage] changed: {last_stage} -> {stage} | arrows g/y/r={count}/{count2}/{count3}")
            last_stage = stage

        count = bar_check_green()
        count2 = bar_check_yellow()
        count3 = bar_check_red()
        count4 = bar_check_all()
        print('Count4 is: ', count4)
        log(f"[arrows] green={count} yellow={count2} red={count3} stage={stage}")

        # ---- 1) Blue first ----
        blue_ok, blue_info = click_color_bgr_in_region(
            target_bgr=BLUE_BGR,
            tol=20,
            region=SEARCH_REGION,
            min_area=50,
            max_tries=2,
            morph_kernel=3,
            post_click_sleep=(0.0, 0.0),
            debug=False,
            use_hsv=True
        )
        if blue_ok:
            log(f"[click] BLUE {fmt_xy(blue_info)}")
            print("[blue] click:", blue_info.get("click_x"), blue_info.get("click_y"), "area:", blue_info.get("area"))
            # debug_color_snapshot(SEARCH_REGION, BLUE_BGR, tol=30, path_prefix="dbg_blue")
            cx, cy = blue_info.get("click_x"), blue_info.get("click_y")
            if cx is not None and cy is not None:
                wait_until_color_gone(
                    target_bgr=BLUE_BGR,
                    tol=20,
                    click_x=cx,
                    click_y=cy,
                    use_hsv=True,
                    morph_kernel=3,
                    clamp_bounds=ACTIVE_BOUNDS,
                    **WAIT_BLUE
                )
            continue

        # ---- 2) PINK next ----
        pink_ok, pink_info = click_color_bgr_in_region(
            target_bgr=PINK_BGR,
            tol=20,
            region=SEARCH_REGION,
            min_area=50,
            max_tries=2,
            morph_kernel=3,
            post_click_sleep=(0.0, 0.0),
            debug=False,
            use_hsv=True
        )
        if pink_ok:
            time.sleep(1.2)
            print("[pink] click:", pink_info.get("click_x"), pink_info.get("click_y"), "area:", pink_info.get("area"))
            log(f"[click] PINK {fmt_xy(pink_info)} stage={stage}")
            arrow_found = wait_for_expected_arrow(stage, timeout=7.0, poll_sleep=0.10)
            if not arrow_found:
                log("[pink] failsafe: expected arrow not seen in 20s, resuming...")
            continue

        # ---- 3) GREEN last ----
        green_ok, green_info = click_color_bgr_in_region(
            target_bgr=GREEN_BGR,
            tol=20,
            region=SEARCH_REGION,
            min_area=50,
            max_tries=2,
            morph_kernel=3,
            post_click_sleep=(0.0, 0.0),
            debug=False,
            use_hsv=True
        )
        if green_ok:
            print("[green] click:", green_info.get("click_x"), green_info.get("click_y"), "area:", green_info.get("area"))
            log(f"[click] GREEN {fmt_xy(green_info)}")
            cx, cy = green_info.get("click_x"), green_info.get("click_y")
            if cx is not None and cy is not None:
                wait_until_color_gone(
                    target_bgr=GREEN_BGR,
                    tol=20,
                    click_x=cx,
                    click_y=cy,
                    use_hsv=True,
                    morph_kernel=3,
                    clamp_bounds=ACTIVE_BOUNDS,
                    **WAIT_GREEN
                )


        # Loop pacing (when nothing is found)
        time.sleep(0.01 if green_ok else 0.01)
