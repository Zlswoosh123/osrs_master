import yaml
import win32gui
import core
import pyautogui
import time
import random
import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np

import functions2 as f2


def gfindWindow(data):  # Find window name and set as active
    global hwnd
    hwnd = win32gui.FindWindow(None, data)
    if hwnd == 0:
        raise Exception(f"Unable to find window: {data}")
    win32gui.SetActiveWindow(hwnd)
    win32gui.MoveWindow(hwnd, 0, 0, 865, 830, True)

with open("pybot-config.yaml", "r") as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)

try:
    gfindWindow(data[0]['Config']['client_title'])
except Exception as e:
    print(e)
    core.printWindows()
    exit()

try:
    x_win, y_win, w_win, h_win = core.getWindow(data[0]['Config']['client_title'])
except Exception as e:
    print(e)
    core.printWindows()
    exit()
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
    f2.ensure_client_foreground()

    # Grab screenshot of region (client-relative)
    img_bgr, (abs_left, abs_top) = f2.grab_client_region(region)
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
    jitter: int = 2,
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
            f2.click_client(t["rel_x"], t["rel_y"], jitter=jitter, move_dur=move_dur)

            if click_type == "right":
                pyautogui.rightClick()

            time.sleep(random.uniform(*post_click_sleep))

    return True, {
        "found": len(matches),
        "clicked": len(targets) * clicks,
        "best_score": matches[0]["score"],
        "targets": targets,
    }

while True:
    # count = f2.Image_count('empty_slot.png')
    # print(count)
    # Click best match inside your inventory area (client-relative coords)
    ok, info = click_image(
        "bracelet.png",
        threshold=0.80,
        region=[624, 465, 814, 737],  # inventory bbox (client-relative)
        debug=True
    )

    # # Click ALL matches found in a region (e.g., click all items of a kind)
    # ok, info = click_image(
    #     "some_item.png",
    #     threshold=0.88,
    #     region=[0, 0, 865, 830],
    #     click_all=True,
    #     debug=True
    # )