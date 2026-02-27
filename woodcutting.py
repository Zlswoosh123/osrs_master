import pyautogui
import win32gui
import time
import yaml
import core
import functions2 as f2
import runtime_vars as v
import random

from functions2 import BLUE_BGR, GREEN_BGR


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

def find_tree():
    print('Looking for tree')
    f2.click_color_bgr_in_region(target_bgr=f2.BLUE_BGR)

def click_basket():
    f2.move_mouse(*f2.inventory_spots[0], min_wait=.1, max_wait=.2, click=True, type='left')

def banking():
    failsafe = 0
    f2.click_color_bgr_in_region(target_bgr=f2.PINK_BGR)
    while f2.icon_check() < 1 and failsafe < 20:
        time.sleep(1)
        failsafe += 1
    time.sleep(.7)
    if f2.icon_check():
        f2.move_mouse(*f2.special_spots['empty'], click=True)  # empty all
        f2.random_wait(.7, 1.5)
        if v.log_basket:
            click_basket()
            time.sleep(.6)
    pyautogui.press('escape')


if __name__ == "__main__":
    if v.log_basket:
        print('Plank Sack is enabled! Must be in slot 1')
    print('Tag trees as blue and banker as pink')
    # Colors (B, G, R)
    Run_Duration_hours = v.run_duration_hours
    t_end = time.time() + (60 * 60 * Run_Duration_hours)
    failsafe = 0
    local_check = time.time() - 1
    spec_timer = time.time() - 1
    left, top, right, bottom = f2.SEARCH_REGION
    last_count = -1
    last_change_time = time.time()
    stuck = 0
    exclude = []
    while time.time() < t_end and stuck <= 6:
        f2.screen_Image(18, 48, 142, 71, 'wc_action.png')
        time.sleep(.1)
        empty_count = f2.Image_count('empty_slot.png')
        text_local = f2.Image_to_Text('thresh', 'wc_action.png')
        print('empty_count is: ', empty_count)
        print('text_local is: ', text_local)

        # green = f2.click_color_bgr_in_region(target_bgr=f2.GREEN_BGR, click=False, region=f2.SEARCH_REGION, tol = 20)[0]
        # if green:
        #     print('Forestry event detected!')
        #     f2.click_color_bgr_in_region(target_bgr=f2.GREEN_BGR, click=True, tol = 20, region=f2.SEARCH_REGION, debug=True)
        #     time.sleep(5)
        #     green = f2.click_color_bgr_in_region(target_bgr=f2.GREEN_BGR, tol = 20, region = f2.SEARCH_REGION, click=False)[0]

        if time.time() > spec_timer and v.wc_spec:
            print('Spec time!')
            spec_wait = random.randint(310, 400)
            f2.move_mouse(*f2.special_spots['spec_orb'], click=True)
            time.sleep(.6)
            f2.click_color_bgr_in_region(target_bgr=BLUE_BGR)
            spec_timer = time.time() + spec_wait

        if empty_count == 0:
            f2.open_inventory_menu()
            time.sleep(.6)
            empty_count = f2.Image_count('empty_slot.png')

        if text_local.strip().lower().replace(",", "") not in ('woodcutting', 'woodcuttin'):
            find_tree()
            time.sleep(3)

        if empty_count != last_count:
            last_count = empty_count
            last_change_time = time.time()
            stuck = 0

            # print('Mined text local is:', mined_text_local)
        # only salvage if stuck for 20 seconds OR count == 0
        if (time.time() - last_change_time >= v.chop_delay) or empty_count == (28 - len(exclude)):
            print("Delay met — clicking tree")
            find_tree()
            last_change_time = time.time()  # reset timer after clicking
            stuck += 1
            time.sleep(6)

        if empty_count == 0:
            if v.log_basket:
                click_basket()
                time.sleep(1)
                empty_count = f2.Image_count('empty_slot.png')
            if empty_count == 0 or empty_count == 1:
                banking()
                empty_count = f2.Image_count('empty_slot.png')
                if empty_count == 0:
                    f2.open_inventory_menu()
                time.sleep(10)
        # Chop wood
        # Click plank sack when full
        # Once inventory is full, drop or bank