import random
import time
import pyautogui
import win32gui
import core
import yaml
from functions import inventory_spots
import functions2 as f2
import runtime_vars as v
from functions2 import click_color_bgr_in_region

global hwnd



def gfindWindow(data):  # find window name returns PID of the window
    global hwnd
    hwnd = win32gui.FindWindow(None, data)
    # hwnd = win32gui.GetForegroundWindow()860
    # print('findWindow:', hwnd)
    win32gui.SetActiveWindow(hwnd)
    # win32gui.ShowWindow(hwnd)
    win32gui.MoveWindow(hwnd, 0, 0, 865, 830, True)


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


def banking():
    failsafe = 0
    f2.click_color_bgr_in_region(target_bgr=f2.PINK_BGR, region=f2.SEARCH_REGION)
    while f2.icon_check(name='empty_all_icon.png', image = 'bank_image.png',  threshold=0.7,
               left=10, top=270, right=400, bottom=550) < 1 and failsafe < 20:
        time.sleep(1)
        failsafe += 1
        if failsafe in [8, 12, 16, 18]:
            f2.click_color_bgr_in_region(target_bgr=f2.PINK_BGR, region=f2.SEARCH_REGION)
    time.sleep(.7)
    if failsafe >= 20:
        print('We had an issue banking! Failsafe triggered')
    else:
        f2.move_mouse(*f2.special_spots['empty_deposit_box'], click=True)  # empty all
        f2.random_wait(.7, 1.5)
    pyautogui.press('escape')

def walk_closer():
    print('Walking closer')
    f2.click_color_bgr_in_region(target_bgr=f2.GREEN_BGR, region=f2.SEARCH_REGION)

def find_shipmate():
    print('Finding shipmate')
    failsafe = 0
    f2.click_color_bgr_in_region(target_bgr=f2.BLUE_BGR, region=f2.SEARCH_REGION)
    while f2.icon_check(name='raw_rabbit.png', image='shop_image.png', threshold=0.7,
                        left=10, top=270, right=400, bottom=550) < 1 and failsafe < 20:
        time.sleep(1)
        failsafe += 1
        if failsafe in [8, 12, 16, 18]:
            f2.click_color_bgr_in_region(target_bgr=f2.BLUE_BGR, region=f2.SEARCH_REGION)
    time.sleep(.7)
    if failsafe >= 20:
        print('We had an issue buying! Failsafe triggered')
    else:
        f2.move_mouse(*f2.shop_spots['row4_item4'], click=True)
        f2.random_wait(.05, .2)
        pyautogui.press('escape')


if __name__ == "__main__":
    print('Tag trees as blue and banker as pink')
    print('Ensure shift-click purchase settings are as desired')
    # Colors (B, G, R)
    Run_Duration_hours = v.run_duration_hours
    t_end = time.time() + (60 * 60 * Run_Duration_hours)
    failsafe = 0
    laps = 0
    while time.time() < t_end and laps < v.max_laps:
        banking()
        f2.hop_worlds()
        f2.random_wait(11,16)
        f2.random_afk_roll(15, wait_min=20, wait_max=90)
        walk_closer()
        f2.random_wait(v.run_to_middle, v.run_to_middle + random.uniform(.6, 1.5))
        find_shipmate()
        walk_closer()
        f2.random_wait(v.run_to_middle, v.run_to_middle + random.uniform(.6, 1.5))
        laps += 1
        f2.random_wait(1,1.2)
        # if f2.click_color_bgr_in_region(target_bgr=f2.DARK_PINK, click=False, tol = 5, region=f2.SEARCH_REGION)[0]:
        #     print('clicked gangplank on accident')
        #     walk_closer()
        #     f2.random_wait(1.5, 2.5)
        #     find_shipmate()
