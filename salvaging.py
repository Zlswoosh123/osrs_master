import pyautogui
import win32gui
import time
import yaml
import core
import functions2 as f2
import runtime_vars as v
from functions2 import SEARCH_REGION
import random


def gfindWindow(data):  # find window name returns PID of the window
    global hwnd
    hwnd = win32gui.FindWindow(None, data)
    # hwnd = win32gui.GetForegroundWindow()860
    #print('findWindow:', hwnd)
    win32gui.SetActiveWindow(hwnd)
    # win32gui.ShowWindow(hwnd)
    win32gui.MoveWindow(hwnd, 0, 0, 865, 830, True)

print('test')
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


def salvage():
    print('Starting salvage!')
    v = f2.click_color_bgr_in_region(target_bgr=f2.YELLOW_BGR, region=f2.SEARCH_REGION, click=False, debug=True, tol=60)[0]
    if v == False:
        f2.click_color_bgr_in_region(target_bgr=f2.DARK_YELLOW_BGR, region=f2.SEARCH_REGION, click=True, debug=True, tol=60)
    else:
        f2.click_color_bgr_in_region(target_bgr=f2.YELLOW_BGR, region=f2.SEARCH_REGION, click=True, debug=True, tol=60)

    print('Ending Salvage')

def clean_loot():
    pyautogui.press('space')
    time.sleep(.7)
    v = f2.click_color_bgr_in_region(target_bgr=f2.BLUE_BGR, region=f2.SEARCH_REGION, click=False, debug=True, tol=60)[0]
    f2.open_inventory_menu()
    time.sleep(.2)
    if v == False:
        f2.click_color_bgr_in_region(target_bgr=f2.DARK_BLUE_BGR, region=f2.SEARCH_REGION, click=True, debug=True, tol=60)
    else:
        f2.click_color_bgr_in_region(target_bgr=f2.BLUE_BGR, region=f2.SEARCH_REGION, click=True, debug=True, tol=60)


def drop_loot(count = 28, exclude = []):
    print('Starting drop loot!')
    nums = [0, 1, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24, 25]
    f2.open_inventory_menu()
    time.sleep(.2)
    pyautogui.keyDown('shift')
    for i in range(count):  # pattern 1
        if i in nums and i not in exclude:
            s = random.uniform(0, 0.07)
            f2.move_mouse(*f2.inventory_spots[i], min_wait=.1, max_wait=.2, click=True, type='left')
    for i in range(count):  # pattern 2
        if i not in nums and i not in exclude:
            s = random.uniform(0, 0.07)
            f2.move_mouse(*f2.inventory_spots[i], min_wait=.1, max_wait=.2, click = True, type= 'left')
    pyautogui.keyUp('shift')
    time.sleep(1)
    salvage()
print('Ending drop loot!')


if __name__ == "__main__":
    # print('Startup Directions: Ensure Crab is tagged pink (all versions) and the entrances (3) are tagged Blue')
    # print('Zoom out far for safety')
    # Colors (B, G, R)
    Run_Duration_hours = v.run_duration_hours
    t_end = time.time() + (60 * 60 * Run_Duration_hours)
    failsafe = 0
    local_check = time.time() - 1
    spec_timer = time.time() - 1
    left, top, right, bottom = f2.SEARCH_REGION
    # old_count = f2.Image_count('small_salvage.png')
    lap = 0
    last_count = -1
    last_change_time = time.time()
    SALVAGE_DELAY = v.SALVAGE_DELAY  # seconds
    salvage_item = v.salvage
    stuck = 0
    exclude = [27, 26, 25, 24, 23, 22, 21, 20, 19]
    salvage()
    while time.time() < t_end:
        count = f2.Image_count(salvage_item)
        empty_count = f2.Image_count('empty_slot.png')
        # print('count is: ', count)
        print('empty_count is: ', empty_count)
        if empty_count == 0:
            f2.open_inventory_menu()
            time.sleep(.6)
            empty_count = f2.Image_count('empty_slot.png')
        if f2.click_color_bgr_in_region(target_bgr=f2.PINK_BGR, click=False)[0]:

            # detect count change
            if empty_count != last_count:
                last_count = empty_count
                last_change_time = time.time()
                stuck = 0

            # only salvage if stuck for 20 seconds OR count == 0
            if (time.time() - last_change_time >= SALVAGE_DELAY) or empty_count == (28-len(exclude)):
                print("Salvage delay met — clicking yellow")
                salvage()
                last_change_time = time.time()  # reset timer after clicking
                stuck += 1
                if stuck > 5:
                    drop_loot(exclude=exclude)
                    stuck = 0
                time.sleep(6)

            failsafe = 0
        else:
            failsafe += 1
            time.sleep(1)
            pyautogui.press('space')
            if failsafe >= 5:
                f2.hop_worlds()
                time.sleep(10)
        if empty_count == 0:
            clean_loot()
            a = 54 - (2.4 * len(exclude))
            b = 60 - (2.4 * len(exclude))
            f2.random_wait(a, b)
            drop_loot(exclude=exclude)
            f2.random_afk_roll(max = 6)
        time.sleep(.6)
        # If (while?) seeing pink, click yellow to start salvage
            # If full, cleanup action
        # If no pink, swap worlds