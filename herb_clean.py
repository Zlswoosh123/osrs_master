import random
import time
import pyautogui
import win32gui
import core
import yaml


import functions
from functions import inventory_spots, move_mouse, click_object

global hwnd
global iflag
global icoord
iflag = False
global newTime_break
newTime_break = False
global timer
global timer_break
global ibreak


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

iflag = False

def random_wait(a=.1, b=.3):
    c = random.uniform(a, b)
    time.sleep(c)



if __name__ == "__main__": # Fixed version for vm
    t = (1314//14) + 1
    while t > 0:
        dur = random.uniform(0.1, 0.25)
        move_mouse(130, 140, 110, 130, dur)  # move to first obj in tab (nest)
        random_wait(.05, .2)
        click_object() # withdraw nest
        random_wait()
        pyautogui.press('escape')
        # click nests here
        for i in range(28):
            s = random.uniform(0.03, 0.1)
            move_mouse(*inventory_spots[i], s)


        move_mouse(425, 430, 345, 365)  # move to banker center screen
        random_wait(.05, .2)
        click_object()
        random_wait(.45,.65)

        move_mouse(480, 490, 625, 635)  # empty all
        random_wait(.05, .2)
        click_object()
        random_wait(.05, .2)
        t -= 1
        print(f'{t} actions remaining')
