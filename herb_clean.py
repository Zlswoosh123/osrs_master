import random
import time
import pyautogui
import win32gui
import core
import yaml


import functions
from functions import inventory_spots

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


def click_object():
    # 3rd item
    # d = random.uniform(0.11, 0.18)
    # time.sleep(d)
    pyautogui.click()
    print('clicked something')

def move_mouse(x1, x2, y1, y2, b=0):
    if b == 0:
        b = random.uniform(0.05, 0.25)
    x_move = random.randrange(x1, x2) - 4
    y_move = random.randrange(y1, y2) - 4
    pyautogui.moveTo(x_move, y_move, duration=b)

def random_wait(a=.1, b=.3):
    c = random.uniform(a, b)
    time.sleep(c)



if __name__ == "__main__": # Fixed version for vm
    t = (1314//14) + 1
    while t > 0:
        dur = random.uniform(0.1, 0.35)
        move_mouse(130, 140, 110, 130, dur)  # move to first obj in tab (nest)
        random_wait(.05, .2)
        click_object() # withdraw nest
        random_wait()
        pyautogui.press('escape')
        # click nests here
        # x1_start = 650
        # x2_start = 660
        # y1_start = 500
        # y2_start = 512

        for i in range(28):
            move_mouse(*inventory_spots[i], True)
        # for i in range(0,28):
        #     quick_dur = random.uniform(.03,.1)
        #     addx = i%4 * 45
        #     addy = i//4 * 40
        #     random_wait(.05, .2)
        #     move_mouse(x1_start + addx, x2_start + addx, y1_start + addy, y2_start + addy, quick_dur)
        #     random_wait(.05, .2)
        #     click_object()


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
