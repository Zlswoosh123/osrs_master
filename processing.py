import pyautogui
import win32gui
import time
import yaml
import core
import functions2 as f2
import runtime_vars as v
import random

from runtime_vars import amount_to_do


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

def interact_processor(run_to_processor_ticks=10, amount_to_process=28, process_ticks=3):
    print('Looking for object')
    f2.click_color_bgr_in_region(target_bgr=f2.GREEN_BGR, tol=10)
    time.sleep(run_to_processor_ticks)
    pyautogui.press('space')
    time.sleep(amount_to_process * process_ticks + random.uniform(.8,2))

def banking():
    failsafe = 0
    f2.click_color_bgr_in_region(target_bgr=f2.PINK_BGR)
    while f2.icon_check() < 1 and failsafe < 20:
        f2.random_wait(.7, 1.5)
        failsafe += 1
        if failsafe == 10:
            f2.click_color_bgr_in_region(target_bgr=f2.PINK_BGR)
    time.sleep(.7)
    if f2.icon_check():
        f2.move_mouse(*f2.special_spots['empty'], click=True)  # empty all
        f2.random_wait(.7, 1.5)
        f2.move_mouse(125, 140, 120, 130, click=True)  # move to first item in bank (grab object)
        f2.random_wait(.7, 1.5)
        pyautogui.press('escape')
    if failsafe >= 20:
        return False
    else:
        return True




if __name__ == "__main__":
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
    count = 0
    while time.time() < t_end and stuck <= 6 and count < amount_to_do:
        if not banking():
            stuck += 1
        else:
            stuck = 0
            f2.random_afk_roll(100)
        f2.random_wait(.3,1)
        if stuck < 1:
            interact_processor(run_to_processor_ticks=5)
            count += 28
            f2.random_afk_roll(100)
