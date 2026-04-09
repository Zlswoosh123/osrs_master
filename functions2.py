import win32gui
import core
import time
import numpy as np
import cv2
import yaml
import pyautogui
import random
from PIL import Image, ImageGrab
import functions
import runtime_vars as v

DEBUG = True  # flip False to quiet logs

BLUE_BGR = (255, 0, 0)
PINK_BGR = (255, 0, 255)
GREEN_BGR = (0, 255, 0)
PURPLE_BGR = (65, 4, 41)
RED_BGR = (0, 0, 255)
YELLOW_BGR = (0, 255, 255)
TEAL_BGR = (255, 255, 0)
ORANGE_BGR = (0, 130, 255)
DARK_YELLOW_BGR = (4, 143, 143)
DARK_BLUE_BGR = (181, 0, 0)
DARK_PINK = (153, 1 , 162)

SEARCH_REGION = [0, 180, 600, 635]
ACTIVE_BOUNDS = (SEARCH_REGION[0], SEARCH_REGION[1], SEARCH_REGION[2], SEARCH_REGION[3])

inventory_spots = [
    (641, 668, 495, 500),  # Spot 1
    (693, 703, 495, 500),  # Spot 2
    (736, 746, 495, 500),  # Spot 3
    (779, 789, 495, 500),  # Spot 4
    (641, 668, 533, 540),  # Spot 5
    (693, 703, 533, 540),  # Spot 6
    (736, 746, 533, 540),  # Spot 7
    (779, 789, 533, 540),  # Spot 8
    (641, 668, 568, 575),  # Spot 9
    (693, 703, 568, 575),  # Spot 10
    (736, 746, 568, 575),  # Spot 11
    (779, 789, 568, 575),  # Spot 12
    (641, 668, 603, 610),  # Spot 13
    (693, 703, 603, 610),  # Spot 14
    (736, 746, 603, 610),  # Spot 15
    (779, 789, 603, 610),  # Spot 16
    (641, 668, 638, 645),  # Spot 17
    (693, 703, 638, 645),  # Spot 18
    (736, 746, 638, 645),  # Spot 19
    (779, 789, 638, 645),  # Spot 20
    (641, 668, 673, 680),  # Spot 21
    (693, 703, 673, 680),  # Spot 22
    (736, 746, 673, 680),  # Spot 23
    (779, 789, 673, 680),  # Spot 24
    (641, 668, 708, 715),  # Spot 25
    (693, 703, 708, 715),  # Spot 26
    (736, 746, 708, 715),  # Spot 27
    (779, 789, 708, 715),  # Spot 28
]

bank_spots = [
    (125, 140, 120,130), # Spot 1
    (175, 190, 120, 130), # Spot 2
    (226, 235, 120, 130), # Spot 3
    (273, 283, 120, 130), # Spot 3
]

shop_spots = {
    'row4_item4':(270, 285, 380, 392)
}

special_spots = {
    'empty':(480, 490, 625, 635),
    'spec_orb':(675, 687, 175, 188),
    'empty_deposit_box':(180, 195, 457, 472)
} # call using: move_mouse(*special_spots["empty"])

worlds = [303, 304, 305, 306, 307, 310, 311, 312, 313, 314, 315, 317, 319, 320, 321, 322, 323,
          324, 325, 327, 328, 329, 331, 332, 333, 334, 336, 337, 338, 339, 340, 341, 342, 343, 344, 346, 347, 348, 349,
          350, 351, 352, 353,
          354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 366, 367, 368, 369, 370, 373, 374, 375, 376, 377, 378,
          386,
          387, 388, 389, 390, 391, 395, 396, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411,
          412, 416, 420, 421, 422, 423, 424, 425, 428, 429, 438, 439, 440, 441, 443, 444, 445, 446, 447,448,
          449, 450, 459, 463, 464, 465, 466, 470, 471, 472, 473, 475, 476, 477, 478, 479, 480, 481, 482, 484, 485, 486, 487, 488, 489, 490,
          491, 492, 493, 494,
          495, 496, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524,
          525, 526, 527,
          528, 529, 531, 532, 534, 535, 536, 538, 541, 542, 543, 544, 545, 546, 547, 550, 551, 556, 557, 558, 559, 562, 563, 564,
          566, 567, 573, 574, 575, 582, 590, 591, 596, 597, 599, 600, 601, 602, 603, 604, 609, 610, 611, 612, 613,
          614, 615, 616, 617, 619, 620, 621, 622, 624, 625, 626, 693, 694, 695]

worlds_us = [305, 306, 307, 313, 314, 315, 320, 321, 322, 323, 324, 329, 331, 332, 337, 338, 339, 340,
             346, 347, 348, 354, 355, 356, 357, 362, 369, 370, 374, 378, 385, 386, 394, 402, 403, 404, 409, 410, 411,
             421, 422, 423, 438, 439, 440, 441, 443, 444, 445, 446, 470, 471, 472, 473, 475, 476, 477, 478, 479, 480, 481, 482,
             484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 538, 541, 542, 543, 544, 545, 546, 547,
             573, 574, 575, 578, 596, 597, 599, 600, 601, 602, 603, 604, 609, 610, 611, 612, 613, 614, 615, 616, 617
             ]

INVENT_CAPACITY = 28
INV_LEFT, INV_TOP, INV_RIGHT, INV_BOTTOM = 620, 460, 814, 737
inv_region = (620, 460, 814, 737)

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

def click_client(x, y, jitter=0, move_dur=(0.001, 0.002)):
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

def random_afk_roll(max = 50, wait_min=30, wait_max=220):
    roll = random.randint(0, max)
    if roll == 1:
        wait = random.randint(wait_min,wait_max)
        print('Afk roll success. Pausing for: ', wait)
        time.sleep(wait)

def region_around_match(template_name: str, threshold: float = 0.70, pad: int = 25, debug: bool = False):
    """
    Find the best match for template_name in the whole client (region=None),
    then return a small padded region [l,t,r,b] around that match bbox.
    """
    matches = find_image(
        template_name=template_name,
        threshold=threshold,
        region=None,
        max_results=1,
        debug=debug
    )
    if not matches:
        return None

    x1, y1, x2, y2 = matches[0]["bbox"]
    return [max(0, x1 - pad), max(0, y1 - pad), x2 + pad, y2 + pad]

def grab_client_region(region=None):
    x0, y0 = get_client_origin()
    ww = globals().get('w_win', 0)
    hh = globals().get('h_win', 0)

    if region is None:
        left, top = x0, y0
        right  = x0 + (ww or 865)
        bottom = y0 + (hh or 830)
    else:
        l, t, r, b = region
        left, top, right, bottom = x0 + l, y0 + t, x0 + r, y0 + b

    im = ImageGrab.grab(bbox=(left, top, right, bottom))

    rgb = np.asarray(im)          # RGB
    bgr = rgb[..., ::-1].copy()   # BGR faster than cvtColor for this conversion
    return bgr, (left, top)

def grab_client_region_bkp(region=None):
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

def find_image(
    template_name: str,
    threshold: float = 0.85,
    region=None,                 # client-relative [l,t,r,b] or None for whole client
    method=cv2.TM_CCOEFF_NORMED,
    max_results: int = 10,
    nms_radius: int = 6,         # suppress near-duplicates
    debug: bool = False,
):
    """
    Find template matches in the client region.

    Returns:
      list of dicts sorted by score desc:
        [{
          "score": float,
          "rel_x": int, "rel_y": int,          # client-relative click point (center)
          "abs_x": int, "abs_y": int,          # absolute screen click point
          "bbox": (x1, y1, x2, y2),            # client-relative bbox of match
        }, ...]
    """
    ensure_client_foreground()

    # Grab screenshot of region (client-relative)
    img_bgr, (abs_left, abs_top) = grab_client_region(region)
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    template = cv2.imread('images/' + template_name, 0)
    if template is None:
        raise FileNotFoundError(f"Template not found: images/{template_name}")

    th, tw = template.shape[:2]  # note: template is gray
    res = cv2.matchTemplate(img_gray, template, method)

    # Collect candidates above threshold
    ys, xs = np.where(res >= threshold)
    if len(xs) == 0:
        return []

    # Build candidates with scores
    cands = []
    for (x, y) in zip(xs, ys):
        score = float(res[y, x])
        cands.append((score, x, y))

    # Sort by score desc
    cands.sort(key=lambda t: t[0], reverse=True)

    # Non-max suppression (very lightweight)
    picked = []
    for score, x, y in cands:
        if len(picked) >= max_results:
            break
        too_close = False
        for ps, px, py in picked:
            if abs(px - x) <= nms_radius and abs(py - y) <= nms_radius:
                too_close = True
                break
        if not too_close:
            picked.append((score, x, y))

    # Convert to click points
    out = []
    reg_l = 0 if region is None else region[0]
    reg_t = 0 if region is None else region[1]

    for score, x, y in picked:
        # match bbox in client-relative coords
        x1 = x + reg_l
        y1 = y + reg_t
        x2 = x1 + tw
        y2 = y1 + th

        # center point (client-relative)
        rel_cx = x1 + tw // 2
        rel_cy = y1 + th // 2

        # absolute screen point
        abs_cx = abs_left + x + tw // 2
        abs_cy = abs_top  + y + th // 2

        out.append({
            "score": score,
            "rel_x": int(rel_cx),
            "rel_y": int(rel_cy),
            "abs_x": int(abs_cx),
            "abs_y": int(abs_cy),
            "bbox": (int(x1), int(y1), int(x2), int(y2)),
        })

    if debug and out:
        best = out[0]
        print(f"[find_image] {template_name} best score={best['score']:.3f} rel=({best['rel_x']},{best['rel_y']})")

    return out

def click_image(
    template_name: str,
    threshold: float = 0.85,
    region=None,                 # client-relative [l,t,r,b]
    clicks: int = 1,
    which: int = 0,              # 0 = best match, 1 = 2nd best, etc.
    click_all: bool = False,
    click_type: str = "left",    # "left" | "right"
    jitter: int = 0,
    move_dur=(0.01, 0.04),
    post_click_sleep=(0.05, 0.15),
    debug: bool = False,
):
    """
    Find image(s) and click.
    Returns (ok: bool, info: dict)
    """
    matches = find_image(
        template_name=template_name,
        threshold=threshold,
        region=region,
        max_results=10,
        debug=debug,
    )

    if not matches:
        if debug:
            print(f"[click_image] No match for {template_name} (th={threshold})")
        return False, {"found": 0}

    # Determine targets
    targets = matches if click_all else [matches[min(which, len(matches)-1)]]

    for t in targets:
        for _ in range(clicks):
            # Use click_client (client-relative), since your window can move.
            click_client(t["rel_x"], t["rel_y"], jitter=jitter, move_dur=move_dur)

            if click_type == "right":
                pyautogui.rightClick()

            time.sleep(random.uniform(*post_click_sleep))

    return True, {
        "found": len(matches),
        "clicked": len(targets) * clicks,
        "best_score": matches[0]["score"],
        "targets": targets,
    }

def hop_worlds(world = None):
    current = world
    new_world = world
    while current == new_world:
        r = random.randint(0, len(worlds) - 1)
        new_world = worlds[r]
    pyautogui.hotkey('ctrl', 'backspace')
    hopmsg = '::hop ' + str(new_world)
    pyautogui.typewrite(hopmsg, .03)
    pyautogui.press('enter')

def screen_Image(left=0, top = 0, right=800, bottom=800, name='screenshot.png'):  # Takes image and gives a name
    # print('Starting screen_image')
    myScreenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    # print('About to screen_image: ', name)
    myScreenshot.save('C:/Users/Zlswo/PycharmProjects/osrs_master/images/' + name)
    # print(f"Screenshot size: {myScreenshot.size}")
    # print(f"Saving region: left={left}, top={top}, right={right}, bottom={bottom}")
    assert 0 <= left < right, "Invalid horizontal coordinates"
    assert 0 <= top < bottom, "Invalid vertical coordinates"

def onscreen_check(name='gemcrab_name.png', image='gc_name_area.png', left=195, top=45, right=420, bottom=110):
    return Image_count(name,image, threshold=0.8, left=left, top=top, right=right, bottom=bottom)


def safe_open(image, png):
    # print('Starting safe_open')
    count = 0
    while image is None and count < 5:
        image = cv2.imread('C:/Users/Zlswo/PycharmProjects/osrs_master/images/' + png)
        print(f'Sleeping until image is created')
        # time.sleep(.3)
        count += 1
    if count == 5:
        print('Safe open failed!')
        return image
    return image

def random_wait(a=.1, b=.3):
    c = random.uniform(a, b)
    time.sleep(c)

def Image_count(object, image='inventshot.png', threshold=0.8,
                left=624, top=465, right=814, bottom=737,
                retries=5, retry_sleep=0.05, pad=2):

    screen_Image(left, top, right, bottom, image)

    # Minimal retry (not safe_open, just basic robustness)
    img_rgb = None
    for _ in range(retries):
        img_rgb = cv2.imread('images/' + image)
        if img_rgb is not None:
            break
        time.sleep(retry_sleep)
    if img_rgb is None:
        return 0

    template = cv2.imread('images/' + object, 0)
    if template is None:
        raise FileNotFoundError(f"Template not found: images/{object}")

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

    count = 0
    while True:
        _, max_val, _, (x, y) = cv2.minMaxLoc(res)
        if max_val < threshold:
            break

        count += 1

        # Suppress a slightly larger region to avoid double-counting
        x0 = max(x - pad, 0)
        y0 = max(y - pad, 0)
        x1 = min(x + w + pad, res.shape[1])
        y1 = min(y + h + pad, res.shape[0])
        res[y0:y1, x0:x1] = -1.0

    return count

def Image_count_bkp(object, image = 'inventshot.png', threshold=0.8, left=624, top=473, right=814, bottom=737):
    # Window 1: object, threshold=0.8, left=0, top=0, right=0, bottom=0
    # Window 2: object, threshold=0.88, left=1000, top=0, right=1920, bottom=800
    counter = 0
    # invent_crop()
    screen_Image(left, top, right, bottom, image)
    img_rgb = cv2.imread('images/' + image)
    # safe_open(img_rgb, image)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('images/' + object, 0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        counter += 1
    return counter

def clamp255(x):
    return max(0, min(255, int(x)))

def move_mouse(x1, x2, y1, y2, click=False, type='left', min_wait = .15, max_wait = .45):
    b = random.uniform(min_wait, max_wait)
    x_move = random.randrange(x1, x2) # - 4
    y_move = random.randrange(y1, y2) # - 4
    pyautogui.moveTo(x_move, y_move, duration=b)
    if click and type == 'left':
        pyautogui.click()
    if click and type == 'right':
        pyautogui.rightClick()
    if click and type == 'drop':
        pyautogui.keyDown('shift')
        pyautogui.click()
        pyautogui.keyUp('shift')

def move_mouse_alt(x1, y1, x2, y2, click=False, type='left', min_wait = .15, max_wait = .45):
    b = random.uniform(min_wait, max_wait)
    x_move = random.randrange(x1, x2) # - 4
    y_move = random.randrange(y1, y2) # - 4
    pyautogui.moveTo(x_move, y_move, duration=b)
    if click and type == 'left':
        pyautogui.click()
    if click and type == 'right':
        pyautogui.rightClick()
    if click and type == 'drop':
        pyautogui.keyDown('shift')
        pyautogui.click()
        pyautogui.keyUp('shift')

def click_color_bgr_in_region(
    target_bgr=(255,173,0),          # teal in BGR (FF00ADFF -> ARGB -> BGR)
    tol=45,                           # per-channel tolerance (try 45–60 while tuning)
    region=SEARCH_REGION,                      # [l,t,r,b] client-relative (None = whole client)
    min_area=30,                      # accept small blobs; we'll still click centroid fallback
    max_tries=3,
    morph_kernel=3,
    post_click_sleep=(0.45, 0.9),
    debug=False,
    use_hsv=True,
    click = True
        # set True if BGR path is flaky
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
            # print('not cnts fired')
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
                if click:
                    click_client(rel_x, rel_y, jitter=0)
                    # click_client(rel_x, rel_y, jitter=0)
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
                # time.sleep(random.uniform(0.15, 0.30))
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

        if click:
            click_client(rel_x, rel_y, jitter=0, move_dur=(.0001, .0002))
        # time.sleep(random.uniform(*post_click_sleep))

        last_info["click_x"] = rel_x
        last_info["click_y"] = rel_y
        return True, last_info

    return False, last_info


def inv_count(name, threshhold = .8):
    return Image_count(name, threshold=threshhold, left=0, top=0, right=810, bottom=750)

def icon_check(name='empty_all_icon.png', image = 'bank_image.png',  threshold=0.7,
               left=462, top=595, right=522, bottom=655):
    return Image_count(name, image, threshold=threshold, left=left, top=top, right=right, bottom=bottom)

def resizeImage(image=None):
    # print('Starting resizeImage -- See resize_quick')
    # resize_quick()
    png = 'images/' + image
    im = Image.open(png)
    # saves new cropped image
    width, height = im.size
    new_size = (width * 7, height * 7)
    im1 = im.resize(new_size)
    # print('Taking textshot.png!')
    im1.save(f'images/{image}_enhanced.png')

def inv_slot_empty(slot = 27):
    left, right, top, bottom = inventory_spots[slot]
    time.sleep(0.12)  # small settle for tab redraw
    count = Image_count(object = 'empty_slot.png', image='slot.png', threshold=0.8, left=left, top=top, right=right, bottom=bottom)
    if count >= 1:
        return True  # Slot is empty
    else:
        return False  # Slot is not empty

# ---- Tab state helpers (cache regions so we don't relocalize every time) ----

_TAB_REGIONS = {}  # e.g. {"inventory": [l,t,r,b], "magic": [l,t,r,b]}

def open_inventory_menu(safe = True, post_action_sleep = .6):
    if safe:
        pyautogui.press('f1')
        time.sleep(.2)
    pyautogui.press('escape')
    time.sleep(post_action_sleep)

def open_magic_menu(safe=True):
    if safe:
        pyautogui.press('f1')
        time.sleep(.15)
    pyautogui.press('f6')
    time.sleep(.05)

def spot_to_bbox_xyxy(spot_xx_yy):
    x1, x2, y1, y2 = spot_xx_yy
    return (x1, y1, x2, y2)

def drop_loot(count = 28, exclude = [v.exclude]):
    print('Starting drop loot!')
    nums = [0, 1, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24, 25]
    open_inventory_menu()
    time.sleep(.2)
    pyautogui.keyDown('shift')
    for i in range(count):  # pattern 1
        if i in nums and i not in exclude:
            s = random.uniform(0, 0.07)
            move_mouse(*inventory_spots[i], min_wait=.1, max_wait=.2, click=True, type='left')
    for i in range(count):  # pattern 2
        if i not in nums and i not in exclude:
            s = random.uniform(0, 0.07)
            move_mouse(*inventory_spots[i], min_wait=.1, max_wait=.2, click = True, type= 'left')
    pyautogui.keyUp('shift')
    time.sleep(1)
print('Ending drop loot!')

def Image_to_Text(preprocess, image, parse_config='--psm 7'):
    resizeImage(image)
    # functions.change_brown_black()

    image = cv2.imread('images/' + image + '_enhanced.png')

    # ✅ Better grayscale for colored text:
    gray = np.max(image, axis=2).astype(np.uint8)
    gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
    gray = cv2.bitwise_not(gray)

    if preprocess == "thresh":
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    if preprocess == "blur":
        gray = cv2.medianBlur(gray, 3)

    if preprocess == 'adaptive':
        gray = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31, 2
        )

    filename = "{}.png".format(functions.os.getpid())
    cv2.imwrite(filename, gray)

    with functions.Image.open(filename) as im:
        text = functions.pytesseract.image_to_string(im, config=parse_config)

    functions.os.remove(filename)
    return text

def first_bank_item(click=True):
    move_mouse(125, 140, 120, 130, click=click)  # move to first item in bank

def withdraw():
    coords = {1:(125, 140, 120, 130),
              2: (175, 190, 120, 130),
              'empty':(480, 490, 625, 635)}


def alch_all_of_item(
    item_img: str,
    inv_region=inv_region,
    threshold=0.80,
    debug=True
) -> int:
    state = True
    item = False
    while state:
        alch_icon, info = click_image(
            'high_alch.png',
            threshold=threshold,
            region=list(inv_region),
            debug=debug
        )
        time.sleep(.05)
        pyautogui.moveRel(-250, -250)
        if not alch_icon:
            print('Had an issue finding alch icon, opening menu')
            move_mouse(705, 706, 758, 759, click=True)
            time.sleep(.1)
            open_magic_menu(safe=False)
            time.sleep(.5)
            alch_icon, info = click_image(
                'high_alch.png',
                threshold=threshold,
                region=list(inv_region),
                debug=debug
            )
            time.sleep(.1)
            pyautogui.moveRel(-250, -250)
            time.sleep(.3)
            item, info = click_image(
                item_img,
                threshold=threshold,
                region=list(inv_region),
                debug=debug
            )
            time.sleep(2.5)
        else:
            time.sleep(.3)
            item, info = click_image(
                item_img,
                threshold=threshold,
                region=list(inv_region),
                debug=debug
            )
            time.sleep(2.5)



        if item:
            pass
        else:
            # No item found, click away to exit high alch
            move_mouse(610, 611, 765, 766, click=True)
            state = False