import datetime
import win32gui
from threading import Thread
import core
import yaml
import math
import tkinter as tk
from tkinter import messagebox


import functions
from dataclasses import dataclass, field
from threading import Thread, Event, Lock
from functions import Image_count, invent_enabled
from functions import image_Rec_clicker, inventory_spots
from functions import screen_Image
from functions import release_drop_item
from functions import drop_item
from functions import Image_to_Text
from functions import invent_crop
from functions import resizeImage
from functions import resize_quick
from PIL import ImageGrab

from functions import random_breaks
from functions import safe_open
from contextlib import contextmanager

import numpy as np
import cv2
import time
import random
import pyautogui

global hwnd
global iflag
global icoord
iflag = False
global timer
import slyautomation_title

inv_cap = random.uniform(14, 17)
print(f'Dropping ore at {inv_cap}')

class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR

@dataclass
class BotState:
    run_duration_hours: float = 4.5
    t_end: float = 0.0
    spot: tuple[int, int] | None = (0, 0)
    actions: str = "None"
    mined_text: str = "Not Mining"
    lock: Lock = field(default_factory=Lock)

    def time_left_str(self) -> str:
        remaining = max(0, self.t_end - time.time())
        return str(datetime.timedelta(seconds=round(remaining)))

# --- Window globals: must always exist
x_win = 0
y_win = 0
w_win = 0
h_win = 0

@contextmanager
def shift_held():
    try:
        pyautogui.keyDown('shift')
        time.sleep(random.uniform(0.06, 0.14))
        yield
    finally:
        time.sleep(random.uniform(0.06, 0.14))
        pyautogui.keyUp('shift')

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
    print("YAML top-level type:", type(data).__name__)
    print("YAML[0] keys:", list(data[0].keys()))
    print("Nav present?:", 'Nav' in data[0])
    if 'Nav' in data[0]:
        print("to_facility_waypoints:", data[0]['Nav'].get('to_facility_waypoints'))
        print("to_mine_waypoints:", data[0]['Nav'].get('to_mine_waypoints'))

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
    # Fallback: try Win32 directly; keep safe defaults if it also fails
    try:
        hwnd_local = win32gui.FindWindow(None, data[0]['Config']['client_title'])
        l, t, r, b = win32gui.GetWindowRect(hwnd_local)
        x_win, y_win, w_win, h_win = l, t, r - l, b - t
    except Exception:
        x_win = y_win = 0
        w_win = h_win = 0

def parse_argb_hex(hex8: str):
    """
    Parse 'FF00ADFF' as ARGB -> return BGR tuple for OpenCV.
    A=FF, R=00, G=AD, B=FF  ==>  BGR = (255, 173, 0)
    """
    s = hex8.strip().lstrip('#')
    if len(s) != 8:
        raise ValueError(f"Expected 8-hex ARGB like 'FF00ADFF', got '{hex8}'")
    a = int(s[0:2], 16)  # ignored
    r = int(s[2:4], 16)
    g = int(s[4:6], 16)
    b = int(s[6:8], 16)
    return (b, g, r)


def timer():
    startTime = time.time()
    return startTime

def ensure_client_foreground():
    """Bring the client window to the front (best-effort; safe if it fails)."""
    try:
        window = win32gui.FindWindow(None, data[0]['Config']['client_title'])
        win32gui.ShowWindow(window, 5)
        win32gui.SetForegroundWindow(window)
        win32gui.SetActiveWindow(window)
    except Exception:
        pass

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


def click_client(x, y, jitter=4, move_dur=(0.12, 0.25)):
    x0, y0 = get_client_origin()
    tx = x0 + x + random.randint(-jitter, jitter)
    ty = y0 + y + random.randint(-jitter, jitter)
    pyautogui.moveTo(tx, ty, duration=random.uniform(*move_dur))
    pyautogui.click()

def print_mouse_pos_relative(seconds=10, hz=10):
    """
    Move your mouse over the target UI to capture client-relative coords.
    """
    ensure_client_foreground()
    x0, y0 = get_client_origin()
    if (x0, y0) == (0, 0):
        print("[calibrate] WARNING: client origin unknown; if your window isn't at (0,0), values will be off.")
    end = time.time() + seconds
    print("\n[calibrate] Move mouse over the UI target…")
    while time.time() < end:
        x, y = pyautogui.position()
        print(f"client-rel: [{x - x0}, {y - y0}]", end='\r')
        time.sleep(1.0 / hz)
    print("\n[calibrate] Done.\n")


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


def match_template_best(bgr_img, tmpl_bgr, method=cv2.TM_CCOEFF_NORMED, scales=(1.0, 0.97, 1.03)):
    """
    Multi-scale template match. Returns (best_score, (x, y), (w, h), scale).
    (x, y) are top-left inside bgr_img.
    """
    h0, w0 = tmpl_bgr.shape[:2]
    best = (-1.0, (0,0), (w0, h0), 1.0)
    for s in scales:
        if s != 1.0:
            tw = max(1, int(round(w0 * s)))
            th = max(1, int(round(h0 * s)))
            tmpl = cv2.resize(tmpl_bgr, (tw, th), interpolation=cv2.INTER_LINEAR)
        else:
            tmpl = tmpl_bgr
            tw, th = w0, h0
        if bgr_img.shape[0] < th or bgr_img.shape[1] < tw:
            continue
        res = cv2.matchTemplate(bgr_img, tmpl, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        score, loc = (max_val, max_loc) if method in (cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR_NORMED) else (1 - min_val, min_loc)
        if score > best[0]:
            best = (score, loc, (tw, th), s)
    return best  # (score, (x, y), (w, h), scale)

def find_template_client(template_path, region=None, threshold=0.86, scales=(1.0, 0.97, 1.03)):
    """
    Searches for template in the given client region.
    Returns (center_x_client, center_y_client, score) or (None, None, 0).
    """
    tmpl = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if tmpl is None:
        print(f"[template] ERROR: cannot read template '{template_path}'")
        return (None, None, 0.0)

    img, (abs_left, abs_top) = grab_client_region(region)
    score, (x, y), (w, h), scale = match_template_best(img, tmpl, scales=scales)
    print(f"[template] '{template_path}' score={score:.3f} scale={scale:.2f}")
    if score < float(threshold):
        return (None, None, score)

    # Convert to client-relative coords
    cx = x + w // 2 + (0 if region is None else region[0])
    cy = y + h // 2 + (0 if region is None else region[1])
    return (cx, cy, score)

def click_template_client(template_path, region=None, threshold=0.86, max_tries=3, jitter=4, pause=(0.35, 0.6)):
    """
    Tries to find and click the template up to max_tries.
    Returns True/False and last score.
    """
    ensure_client_foreground()
    last_score = 0.0
    for i in range(max_tries):
        cx, cy, score = find_template_client(template_path, region=region, threshold=threshold)
        last_score = score
        if cx is not None:
            click_client(cx, cy, jitter=jitter)
            time.sleep(random.uniform(*pause))
            return True, score
        time.sleep(random.uniform(0.2, 0.35))
    return False, last_score


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
    target_bgr=(255,173,0),          # teal in BGR (from FF00ADFF BGRA)
    tol=30,                           # ±tolerance per channel
    region=None,                      # [l,t,r,b] client-relative
    min_area=120,                     # minimum contour area to accept
    max_tries=3,
    morph_kernel=3,
    debug=False
):
    """
    Find a blob of the target BGR color in the region and click its centroid.
    Returns (ok:bool, info:dict).
    """
    ensure_client_foreground()
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (morph_kernel, morph_kernel))
    last_info = {}
    for attempt in range(max_tries):
        img_bgr, (abs_left, abs_top) = grab_client_region(region)  # uses your existing grab
        B, G, R = target_bgr
        lower = np.array([clamp255(B - tol), clamp255(G - tol), clamp255(R - tol)], dtype=np.uint8)
        upper = np.array([clamp255(B + tol), clamp255(G + tol), clamp255(R + tol)], dtype=np.uint8)

        mask = cv2.inRange(img_bgr, lower, upper)
        if morph_kernel > 1:
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, k, iterations=1)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k, iterations=1)

        # Find largest contour
        cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not cnts:
            last_info = {"attempt": attempt+1, "area": 0, "found": 0}
            time.sleep(random.uniform(0.15, 0.30))
            continue

        c = max(cnts, key=cv2.contourArea)
        area = cv2.contourArea(c)
        last_info = {"attempt": attempt+1, "area": float(area), "found": len(cnts)}

        if area < float(min_area):
            # Too small; try again
            if debug:
                print(f"[color] small area={area:.1f} < {min_area}, retrying…")
            time.sleep(random.uniform(0.15, 0.30))
            continue

        M = cv2.moments(c)
        if M["m00"] == 0:
            time.sleep(random.uniform(0.1, 0.2))
            continue
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        # convert to client-relative coords
        rel_x = cx + (0 if region is None else region[0])
        rel_y = cy + (0 if region is None else region[1])

        if debug:
            print(f"[color] click @ client-rel [{rel_x}, {rel_y}] area={area:.1f}")

        click_client(rel_x, rel_y, jitter=4)
        time.sleep(random.uniform(0.45, 0.8))
        return True, last_info

    return False, last_info

def wait_until_still(region, settle_ms=250, timeout_s=8, check_hz=10, delta_thresh=8000):
    img_prev, _ = grab_client_region(region)
    last_move = time.time()
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        time.sleep(1.0 / check_hz)
        img_cur, _ = grab_client_region(region)
        diff = cv2.absdiff(img_prev, img_cur)
        if int(diff.sum()) < delta_thresh:
            if (time.time() - last_move) * 1000 >= settle_ms:
                return True
        else:
            last_move = time.time()
        img_prev = img_cur
    return False

def click_waypoints(pts, jitter=4, pause=(0.45, 0.75), long_every=None, long_extra=(0.4, 0.8)):
    """
    Walk through client-relative waypoints with human-like pacing.
    If Nav.minimap_region exists, wait for 'stillness' after each click; else sleep.
    """
    ensure_client_foreground()
    mm = data[0].get('Nav', {}).get('minimap_region')
    for i, (x, y) in enumerate(pts):
        click_client(x, y, jitter=jitter)

        # base delay
        base = random.uniform(*pause)
        if long_every and (i + 1) % int(long_every) == 0 and (i + 1) < len(pts):
            base += random.uniform(*long_extra)

        if mm:
            ok = wait_until_still(mm, settle_ms=300, timeout_s=7)
            if not ok:
                time.sleep(base)  # fallback if we timed out
        else:
            time.sleep(base)



def Miner_Image_quick(left = 0, top = 150, right = 800, bottom = 770):
    # left = 150
    # top = 150
    # right = 650
    # bottom = 750
    print('About to Miner_image_quick')
    im = ImageGrab.grab(bbox=(left, top, right, bottom))
    print(f"Saving region: left={left}, top={top}, right={right}, bottom={bottom}")
    im.save('images/miner_img.png', 'png')

INVENT_CAPACITY = 28
INV_LEFT, INV_TOP, INV_RIGHT, INV_BOTTOM = 620, 460, 812, 735

def bank_prompt():
    """
    Blocking pop-up: tells you to bank manually, then choose to continue or stop.
    Returns True to continue, False to stop.
    """
    # Belt & suspenders: make sure Shift isn’t stuck down
    try:
        release_drop_item()
    except Exception:
        pass

    msg = ("Inventory full.\n\n"
           "Bank manually now, then choose:\n"
           "• Repeat: continue the script\n"
           "• Cancel: stop the script")
    choice = pyautogui.confirm(text=msg, title='Banking Needed', buttons=['Repeat', 'Cancel'])
    return choice == 'Repeat'

def turn_in_cycle() -> bool:
    """
    Navigate -> (optional) open -> color-click deposit -> verify -> return.
    Uses ARGB teal from YAML and color detection.
    """
    nav = data[0].get('Nav', {}) or {}
    ti  = data[0].get('TurnIn', {}) or {}

    to_facility = nav.get('to_facility_waypoints') or []
    to_mine     = nav.get('to_mine_waypoints') or []
    if not to_facility or not to_mine:
        print("[turn-in] Missing waypoints → simple sleep fallback")
        time.sleep(2.0); time.sleep(1.2); time.sleep(1.6)
        return True

    # pacing from YAML
    step_pause      = tuple(nav.get('step_pause', [1.3, 2.0]))
    step_pause_back = tuple(nav.get('step_pause_back', list(step_pause)))
    long_every      = nav.get('long_pause_every', None)
    long_extra      = tuple(nav.get('long_pause_extra', [0.6, 1.2]))

    # deposit config
    # Support both names for backward compatibility (see item 4):
    deposit_hex_key = 'deposit_argb' if 'deposit_argb' in ti else 'deposit_bgra'
    deposit_hex     = ti.get(deposit_hex_key, 'FF00ADFF')
    target_bgr      = parse_argb_hex(deposit_hex) if deposit_hex_key == 'deposit_argb' else parse_bgra_hex(deposit_hex)

    deposit_region   = ti.get('deposit_region')                  # [l,t,r,b] or None
    deposit_tol      = int(ti.get('deposit_tol', 35))
    deposit_min_area = int(ti.get('deposit_min_area', 120))
    morph_kernel     = int(ti.get('deposit_morph_kernel', 3))

    open_xy   = ti.get('open_click')   # optional
    close_xy  = ti.get('close_click')  # optional
    dep_xy_fb = ti.get('deposit_click')  # optional fixed fallback

    pauses         = ti.get('pauses', {}) or {}
    p_open         = float(pauses.get('after_open', 0.6))
    p_pre_deposit  = float(pauses.get('before_deposit', 0.2))
    p_post_deposit = float(pauses.get('after_deposit', 0.9))
    p_close        = float(pauses.get('after_close', 0.2))

    # run toggle (optional)
    run_key = data[0]['Config'].get('run_toggle_key')

    # Count before (for verification)
    try:
        before = count_tracked_inventory()
    except Exception:
        before = None

    ensure_client_foreground()
    if run_key:
        pyautogui.press(run_key); time.sleep(0.15)

    # 1) Go there (paced)
    print("[turn-in] Navigating to facility...")
    # click_waypoints(to_facility, pause=step_pause, long_every=long_every, long_extra=long_extra)

    # 2) Open (optional)
    if open_xy:
        print("[turn-in] Opening turn-in panel…")
        click_client(open_xy[0], open_xy[1], jitter=5)
        time.sleep(p_open)

    # 3) Deposit via color detection (primary)
    print("[turn-in] Color-click deposit (teal)…")
    time.sleep(p_pre_deposit)
    ok, info = click_color_bgr_in_region(
        target_bgr=target_bgr,
        tol=deposit_tol,
        region=deposit_region,
        min_area=deposit_min_area,
        max_tries=3,
        morph_kernel=morph_kernel,
        debug=False
    )
    time.sleep(3)  # EXTRA post-click pause here
    if not ok:
        print(f"[turn-in] Color not found in region (tries={info.get('attempt','?')}, area={info.get('area',0)}). "
              f"Trying whole-client fallback…")
        ok, info = click_color_bgr_in_region(
            target_bgr=target_bgr,
            tol=max(deposit_tol, 45),
            region=None,
            min_area=max(60, int(deposit_min_area * 0.6)),
            max_tries=2,
            morph_kernel=morph_kernel,
            debug=False
        )

    if not ok and dep_xy_fb:
        print("[turn-in] Fallback: fixed deposit_click")
        click_client(dep_xy_fb[0], dep_xy_fb[1], jitter=5)
        time.sleep(p_post_deposit)
    else:
        time.sleep(p_post_deposit)

    # 4) Close (optional)
    if close_xy:
        print("[turn-in] Closing panel…")
        click_client(close_xy[0], close_xy[1], jitter=3)
        time.sleep(p_close)

    # 5) Verify inventory reduced; one retry if not
    try:
        after = count_tracked_inventory()
        if before is not None:
            if after < before:
                print(f"[turn-in] Inventory decreased: {before} -> {after} ✔")
            else:
                print(f"[turn-in] WARNING: inventory not reduced ({before} -> {after}). Retrying deposit once…")
                ok2, _ = click_color_bgr_in_region(
                    target_bgr=target_bgr,
                    tol=min(60, deposit_tol + 10),
                    region=deposit_region,
                    min_area=max(60, int(deposit_min_area * 0.6)),
                    max_tries=2,
                    morph_kernel=morph_kernel,
                    debug=False
                )
                if not ok2 and dep_xy_fb:
                    click_client(dep_xy_fb[0], dep_xy_fb[1], jitter=5)
                    time.sleep(0.8)
                final = count_tracked_inventory()
                print(f"[turn-in] Post-retry inventory: {after} -> {final}")
    except Exception:
        pass

    # 6) Return (paced)
    print("[turn-in] Returning to mine…")
    click_waypoints(to_mine, pause=step_pause_back, long_every=long_every, long_extra=long_extra)

    if run_key:
        pyautogui.press(run_key); time.sleep(0.1)
    return True


def Miner_Image():
    screen_Image(0, 900, 0, 900, 'images/miner_img.png')
    print('Taking Miner_image photo)')

def _half_pair_order():
    """
    Build indices for the 4x7 grid such that we click:
      Left half pairs:  (1,2), (5,6), (9,10), ..., (25,26)
      Right half pairs: (3,4), (7,8), (11,12), ..., (27,28)

    inventory_spots is 0-based (0..27), but comments label them 1..28.
    Row r has indices [r*4 + 0, r*4 + 1, r*4 + 2, r*4 + 3]
    """
    order = []

    rows = 7
    # Left half first: columns 0 & 1
    for r in range(rows):
        order.append(r*4 + 0)  # spot 1,5,9,...
        order.append(r*4 + 1)  # spot 2,6,10,...

    # Right half next: columns 2 & 3
    for r in range(rows):
        order.append(r*4 + 2)  # spot 3,7,11,...
        order.append(r*4 + 3)  # spot 4,8,12,...

    return order  # length 28

def drop_ore():
    """
    Shift-clicks inventory slots in a deterministic pattern:
      (1,2) -> (5,6) -> ... -> (25,26) -> (3,4) -> (7,8) -> ... -> (27,28)
    Uses static rectangles from functions.inventory_spots.
    """
    global actions
    actions = "dropping ores (halves pattern)"

    order = _half_pair_order()              # fixed sequence of slot indices
    boxes  = [inventory_spots[i] for i in order]

    drop_item()  # holds Shift
    try:
        for (x1, x2, y1, y2) in boxes:
            # pick a random point *inside* the small box to avoid robotic exact pixels
            tx = random.randint(x1, x2)
            ty = random.randint(y1, y2)
            pyautogui.moveTo(tx, ty, duration=random.uniform(0.05, 0.15))
            pyautogui.click(tx, ty, duration=random.uniform(0.03, 0.08), button="left")
            time.sleep(random.uniform(0.01, 0.05))  # slight human-like pacing
        return "drop ore done"
    finally:
        release_drop_item()  # ALWAYS release Shift

def findarea_single(ore, cropx, cropy):
    Miner_Image_quick()
    image = cv2.imread(r"images/miner_img.png")
    safe_open(image, 'miner_img.png')

    # B, G, R ranges
    tin = ([103, 86, 65], [145, 133, 128])
    copper = ([35, 70, 120], [65, 110, 170])
    coal = ([20, 30, 30], [30, 50, 50])
    iron = ([15, 20, 40], [25, 40, 70])
    iron2 = ([17, 20, 42], [25, 38, 70])
    clay = ([50, 105, 145], [60, 125, 165])
    red = ([0, 0, 180], [80, 80, 255])
    green = ([0, 180, 0], [80, 255, 80])
    amber = ([0, 160, 160], [80, 255, 255])
    ore_list = [tin, copper, coal, iron, iron2, clay, red, green, amber]

    lower, upper = ore_list[ore]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)
    ret, thresh = cv2.threshold(mask, 40, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if not contours:
        # No target found
        return None

    # Largest contour
    c = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)

    # Guard against tiny boxes
    w = max(w, 6)
    h = max(h, 6)

    tx = random.randrange(x + 2, x + w - 1) + cropx
    ty = random.randrange(y + 2, y + h - 1) + cropy

    pyautogui.moveTo(tx, ty, duration=random.uniform(0.1, 0.3))
    pyautogui.click(duration=random.uniform(0.07, 0.11))
    return (tx, ty)

def count_gems():
    return Image_count('gem_icon.png', threshold=0.8, left=0, top=0, right=800, bottom=750)

def count_geo():
    return Image_count('geo_icon.png', threshold=0.8, left=0, top=0, right=800, bottom=750)

def count_gems2():
    return Image_count('gem_icon2.png', threshold=0.8, left=0, top=0, right=800, bottom=750)

def inv_count(name):
    return Image_count(name + '_ore.png', threshold=0.8, left=0, top=0, right=800, bottom=750)

def timer_printer(state: BotState, stop_event: Event):
    # prints once per second until stop_event is set or time expires
    while not stop_event.is_set() and time.time() < state.t_end:
        with state.lock:
            tl = state.time_left_str()
            spot = state.spot
            mined = state.mined_text
            act = state.actions
        print(
            bcolors.OK +
            f'\rtime left: {tl} | status: {mined}',
            end=''
        )
        time.sleep(.3)

TRACKED_ORES = ['1kg', '2kg', '5kg', '10kg']

def count_tracked_inventory():
    invent_crop()  # refresh screenshot
    total = 0
    for ore in TRACKED_ORES:
        cnt = inv_count(ore)
        total += cnt
    print('Invent count is: ', total)
    return total

def count_items():
    global Run_Duration_hours
    t_end = time.time() + (60 * 60 * Run_Duration_hours)
    while time.time() < t_end:
        global ore, powerlist, mined_text
        time.sleep(0.1)

# def print_progress(time_left, spot, mined_text, powerlist, ore, actions):
    # print(bcolors.OK +
    #     f'\rtime left: {time_left} | coords: {spot} | status: {mined_text} | {actions}',
    #     end='')

def powerminer_text(ore, num, Take_Human_Break=False, Run_Duration_hours=5):
    global inv_cap, powerlist
    runelite = functions.runelite
    powerlist = ['tin', 'copper', 'coal', 'iron', 'gold', 'clay', 'red', 'green', 'amber']

    # INIT SHARED STATE
    state = BotState(run_duration_hours=Run_Duration_hours)
    state.t_end = time.time() + (60 * 60 * state.run_duration_hours)

    # Start printer thread
    stop_event = Event()
    t1 = Thread(target=timer_printer, args=(state, stop_event), daemon=True)
    t1.start()

    print("Mine Ore Selected:", powerlist[ore])
    spot = (0, 0)  # local cursor target

    while time.time() < state.t_end:
        # --- inventory visibility + decision logic ---
        inventory = count_tracked_inventory()
        inv_check = 0
        if inventory == 0 and inv_check == 0:
            # Try once to reveal inventory (prefer F1 if bound; Esc if you truly rely on it)
            with state.lock:
                state.actions = 'opening inventory'
            try:
                window = win32gui.FindWindow(None, runelite)
                win32gui.ShowWindow(window, 5)
                win32gui.SetForegroundWindow(window)
                win32gui.SetActiveWindow(window)
            except Exception:
                pass

            # Prefer a specific tab key over Esc to avoid toggling closed; adjust if needed
            pyautogui.press('esc')
            time.sleep(0.3)
            inventory = count_tracked_inventory()
            inv_check += 1

        print(f"Inventory has {inventory} tracked ores")

        with state.lock:
            state.actions = 'None'

        if BANK_MODE:
            # === PHASE 1: replace manual popup with automated stub ===
            if inventory >= BANK_THRESHOLD:
                with state.lock:
                    state.actions = 'turn-in'
                ok = turn_in_cycle()
                if not ok:
                    print("\nTurn-in failed; stopping.")
                    break  # exit mining loop
                inv_cap = random.uniform(14, 17)
                print(f"Resuming. Next auto-drop threshold (if used later): {inv_cap}")
                # After turn-in, continue loop (return to mining section)
                continue
            # === END PHASE 1 ===
        else:
            # Powerminer (auto-drop) flow
            if inventory >= inv_cap:
                with state.lock:
                    state.actions = 'dropping (grid)...'
                result = drop_ore()
                with state.lock:
                    state.actions = result
                time.sleep(random.uniform(0.1, 0.2))  # light pause
                inv_cap = random.uniform(14, 17)
                print(f'Dropping ore at {inv_cap}')

        resize_quick()
        resizeImage()
        mined_text_local = Image_to_Text('thresh', 'textshot.png').strip().lower()

        if mined_text_local not in ('mining', 'mininq'):
            mined_text_local = 'Not Mining'
            # Find a target; may return None
            # new_spot = findarea_single(num, 150, 150)
            new_spot = findarea_single(num, 0, 150)
            if new_spot is None:
                time.sleep(random.uniform(0.01, 0.02))
            else:
                spot = new_spot
                if Take_Human_Break:
                    time.sleep(random.triangular(0.05, 6, 0.5))
            time.sleep(random.uniform(1.5, 1.8))  # ~1–1.5s pause to let mining start

        else:
            mined_text_local = 'Mining'

        with state.lock:
            state.mined_text = mined_text_local
            state.spot = spot

    # Stop the printer thread
    stop_event.set()
    t1.join(timeout=1.0)

spot = (0, 0)
actions = 'None'
mined_text = 'Not Mining'
time_left = 0
BANK_MODE = True          # set True to enable turn-in stub (Phase 1)
BANK_THRESHOLD = 27      # trigger when inventory has 27 or more items
#-------------------------------

powerlist = ['tin', 'copper', 'coal', 'iron', 'gold', 'clay', 'red', 'green', 'amber']


#-------------------------------


if __name__ == "__main__":

    # ----- ORE -------
    tin = 0
    copper = 1
    coal = 2
    iron = 3
    gold = 4
    clay = 5

    # ----- OBJECT MARKER COLOR ------
    red = 6
    green = 7
    amber = 8

    # --------- CHANGE TO RUN FOR AMOUNT OF HOURS ----------------
    Run_Duration_hours = 1.5

                # | ore | marker color | take break | how long to run for in hours
    powerminer_text(iron, red, Take_Human_Break=True, Run_Duration_hours=Run_Duration_hours)
