import win32gui
import core
import yaml
from functions import Image_count, invent_enabled, move_mouse, click_object
from PIL import ImageGrab

import numpy as np
import cv2
import time
import random
import pyautogui

global hwnd
global iflag
global icoord
iflag = False


inv_cap = random.uniform(14, 17)
print(f'Dropping ore at {inv_cap}')

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

def parse_bgra_hex(hex8: str):
    """
    Parse 'FF00ADFF' as BGRA (common for Windows screenshots).
    Returns (B, G, R). Alpha is ignored.
    """
    s = hex8.strip().lstrip('#')
    if len(s) != 8:
        raise ValueError(f"Expected 8-hex BGRA like 'FF00ADFF', got '{hex8}'")
    b = int(s[0:2], 16)
    g = int(s[2:4], 16)
    r = int(s[4:6], 16)
    # a = int(s[6:8], 16)
    return (b, g, r)

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
    use_hsv=False                     # set True if BGR path is flaky
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
                return True, {"attempt": attempt+1, "area": 0.0, "found": 0, "fallback": "nonzero-centroid"}
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
        return True, last_info

    return False, last_info

def inv_count(name):
    return Image_count(name + '.png', threshold=0.8, left=0, top=0, right=810, bottom=750)

def icon_check(name='empty_all_icon'):
    return Image_count(name + '.png','bank_image', threshold=0.7, left=388, top=603, right=552, bottom=648)

def random_wait(a=.1, b=.3):
    c = random.uniform(a, b)
    time.sleep(c)

def withdraw_ore(lap, ore = 'mithril'):
    print('Starting withdraw_ore')
    count = 0
    retry = 0
    move_mouse(650, 665, 500, 515)  # move to first obj in inv (load coal sack)
    random_wait(.15, .3)
    click_object()
    random_wait(.15, .3)
    while count < 27:
        if ore == 'mithril':
            if lap > 3:
                lap = lap - 3
            if lap % 2 == 0 or lap % 3 == 0:
                move_mouse(125, 140, 120,130) # move to first item in bank (grab mithril)
                random_wait(.15, .3)
                click_object()
                random_wait(.15, .3)
            else:
                move_mouse(175, 190, 120, 130) # move to 2nd item in bank (grab coal)
                random_wait(.15, .3)
                click_object()
                random_wait(.15, .3)

        if ore == 'iron':
            move_mouse(125, 140, 120, 130)  # move to first item in bank (grab mithril)
            random_wait(.15, .3)
            click_object()
            random_wait(.15, .3)

        if ore == 'adamant':
            if lap % 2==0:
                move_mouse(125, 140, 120,130) # move to first item in bank (grab mithril)
                random_wait(.15, .3)
                click_object()
                random_wait(.15, .3)
            else:
                move_mouse(175, 190, 120, 130) # move to 2nd item in bank (grab coal)
                random_wait(.15, .3)
                click_object()
                random_wait(.15, .3)

        if ore == 'rune':
            if lap > 5:
                lap = lap - 5
            if lap % 3 == 0 or lap % 5 == 0:
                move_mouse(125, 140, 120, 130)  # move to first item in bank (grab mithril)
                random_wait(.15, .3)
                click_object()
                random_wait(.15, .3)
            else:
                move_mouse(175, 190, 120, 130) # move to 2nd item in bank (grab coal)
                random_wait(.15, .3)
                click_object()
                random_wait(.15, .3)
        time.sleep(1)
        count = inv_count('coal_ore')
        print('We tried withdrawing ore and have: ', count)
        retry += 1
        if retry >= 5:
            break
    pyautogui.press('escape')
    print('Ending withdraw_ore')
    return lap

def conveyor_belt():
    print('Starting conveyor_belt')
    # Finding conveyor belt
    click_color_bgr_in_region(
        target_bgr=(255,173,0),
        tol=30,  # try 30–45 if needed
        region= [0, 0, 600, 750],
        min_area=50,  # try 60–120
        max_tries=3,
        morph_kernel=3,  # 3 or 5
        debug=False  # write dbg_deposit_region.png/dbg_deposit_mask.png
    )
    time.sleep(8)
    count = inv_count('coal_ore')
    print('Count is: ', count)
    retry = 0
    # Checking to ensure we deposited, retry if not
    if count != 0:
        while count != 0:
            retry += 1
            print('We couldnt deposit for some reason, retrying! Number: ', retry)
            # time.sleep(3)
            click_color_bgr_in_region(
                target_bgr=(255, 173, 0),
                tol=30,  # try 30–45 if needed
                region=[0, 0, 600, 750],
                min_area=50,  # try 60–120
                max_tries=3,
                morph_kernel=3,  # 3 or 5
                debug=False  # write dbg_deposit_region.png/dbg_deposit_mask.png
            )
            time.sleep(6)
            count = inv_count('coal_ore')
            print('Retry count is: ', count)
            if retry >= 5:
                print('Retries failed, breaking!')
                break

    #Withdraw coal from sack and drop on belt
    move_mouse(650, 665, 500, 515)  # move to first obj in inv (next box)
    random_wait(.05, .2)
    click_object()
    random_wait(.05, .2)

    click_color_bgr_in_region(
        target_bgr=(255, 173, 0),
        tol=30,  # try 30–45 if needed
        region=[0, 0, 600, 750],
        min_area=50,  # try 60–120
        max_tries=3,
        morph_kernel=3,  # 3 or 5
        debug=False  # write dbg_deposit_region.png/dbg_deposit_mask.png
    )
    count = inv_count('coal_ore')
    print('Count is: ', count)
    retry = 0
    # Checking to ensure we deposited, retry if not
    if count != 0:
        while count != 0:
            retry += 1
            print('We couldnt deposit for some reason, retrying! Number: ', retry)
            time.sleep(3)
            click_color_bgr_in_region(
                target_bgr=(255, 173, 0),
                tol=30,  # try 30–45 if needed
                region=[0, 0, 600, 750],
                min_area=50,  # try 60–120
                max_tries=3,
                morph_kernel=3,  # 3 or 5
                debug=False  # write dbg_deposit_region.png/dbg_deposit_mask.png
            )
            time.sleep(3)
            count = inv_count('coal_ore')
            print('Retry count is: ', count)
            if retry >= 5:
                print('Retries failed, breaking!')
                break

    print('Ending conveyor_belt')

def pickup_bars():
    print('Starting pickup_bars')
    time.sleep(2)
    click_color_bgr_in_region(
        target_bgr=(240, 0, 255),
        tol=30,  # try 30–45 if needed
        region=[0, 0, 600, 750],
        min_area=50,  # try 60–120
        max_tries=3,
        morph_kernel=3,  # 3 or 5
        debug=False  # write dbg_deposit_region.png/dbg_deposit_mask.png
    )
    time.sleep(6)
    pyautogui.press('space')
    time.sleep(1)
    bars = inv_count('bar')
    retry = 0
    print('Bar count is: ', bars)

    if bars < 25:
        while bars < 25:
            retry += 1
            print('We couldnt pickup bars for some reason, retrying! Number: ', retry)
            click_color_bgr_in_region(
                target_bgr=(240, 0, 255),
                tol=30,  # try 30–45 if needed
                region=[0, 0, 600, 750],
                min_area=50,  # try 60–120
                max_tries=3,
                morph_kernel=3,  # 3 or 5
                debug=False  # write dbg_deposit_region.png/dbg_deposit_mask.png
            )
            time.sleep(3)
            pyautogui.press('space')
            time.sleep(1)
            bars = inv_count('bar')
            print('Retry count for bars is is: ', bars)
            if retry >= 5:
                print('Retries failed, breaking!')
                break
    print('Ending pickup_bars')

def deposit():
    icon = 0
    retry = 0
    print('Starting Deposit')
    click_color_bgr_in_region(
        target_bgr=(0, 0, 255),
        tol=30,  # try 30–45 if needed
        region=[0, 230, 815, 750],
        min_area=50,  # try 60–120
        max_tries=3,
        morph_kernel=3,  # 3 or 5
        debug=True  # write dbg_deposit_region.png/dbg_deposit_mask.png
    )
    time.sleep(6)
    icon = icon_check()
    if icon >= 1:
        move_mouse(480, 490, 625, 635)  # empty all
        random_wait(.05, .2)
        click_object()
        random_wait(.05, .2)

    while icon ==0 and retry < 5:
        retry += 1
        click_color_bgr_in_region(
            target_bgr=(0, 0, 255),
            tol=30,  # try 30–45 if needed
            region=[0, 230, 815, 750],
            min_area=50,  # try 60–120
            max_tries=3,
            morph_kernel=3,  # 3 or 5
            debug=True  # write dbg_deposit_region.png/dbg_deposit_mask.png
        )
        time.sleep(5)
        icon = icon_check()
        if icon >= 1:
            move_mouse(480, 490, 625, 635)  # empty all
            random_wait(.05, .2)
            click_object()
            random_wait(.05, .2)

    bars = inv_count('bar')

    print('Bar count is: ', bars)

    print('Ending Deposit')
    return retry



time_left = 0
#-------------------------------

if __name__ == "__main__":
    # --------- CHANGE TO RUN FOR AMOUNT OF HOURS ----------------
    Run_Duration_hours = .5
    t_end = time.time() + (60 * 60 * Run_Duration_hours)
    ore = 'mithril'
    lap = 1
    while time.time() < t_end:
        print('Starting lap ', lap)
    # Withdraw ore
        lap = withdraw_ore(lap=lap, ore=ore)
        ## In bank, Click Coal
        ## Fill on coal sack
        ## Click other ore, esc
    # Click turn in
        conveyor_belt()
        ## Find teal (FF00ADFF, 255, 173, 0) and click it
        ## Ensure ore deposited check
        ## Withdraw coal from coal sack
        ## Find teal (FF00ADFF) and click it
        ## Ensure coal deposited check
        ## Wait for ore to land
    # Pickup bars
        if ore == 'mithril':
            if lap > 3:
                lap = lap - 3
            if lap % 2 == 0 or lap % 3 == 0:
                pickup_bars()

        if ore == 'iron':
            pickup_bars()

        if ore == 'adamant':
            if lap % 2 == 0:
                pickup_bars()

        if ore == 'rune':
            if lap > 5:
                lap = lap - 5
            if lap % 3 == 0 or lap % 5 == 0:
                pickup_bars()



        ## Click yellow (FFFFFF00, 241, 0, 255) and click it
        ## Ensure bars are in inventory check
    # Deposit bars by clicking on bank
        retry = deposit()
        if retry >= 5:
            print('Had issues depositing, crashing script')
            break
        print('Ending lap ', lap)
        lap +=1
    ## Find red (FFFF0000, 0, 0, 255) and click it
    ## Ensure bank is open check
    ## Deposit Click bars in inventory to deposit
