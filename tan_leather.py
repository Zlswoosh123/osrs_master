import random
import time
import pyautogui
import win32gui
import core
import yaml


import functions

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
    d = random.uniform(0.11, 0.18)
    time.sleep(d)
    pyautogui.click()
    print('clicked something')

def move_mouse(x1, x2, y1, y2):
    b = random.uniform(0.1, 0.3)
    x_move = random.randrange(x1, x2) + 5
    y_move = random.randrange(y1, y2) + 5
    pyautogui.moveTo(x_move, y_move, duration=b)

def random_wait(a=.1, b=.3):
    c = random.uniform(a, b)
    time.sleep(c)



if __name__ == "__main__":
    t = 420
    while t > 0:
        n = 5
        wait_roll = random.randint(1, 1000)
        wait_time_long = random.randint(45, 260)
        wait_time_short = random.randint(15, 60)
        print(f'The anti-ban dice have been thrown! You rolled a {wait_roll}')

        if wait_roll % 200 == 0:
            print(f'Weve initiated a long wait for anti-ban for {wait_time_long}s')
            time.sleep(wait_time_long)
            n = 5
        if wait_roll % 20 == 0:
            print(f'Weve initiated a short wait for anti-ban for {wait_time_short}s')
            time.sleep(wait_time_short)
            n = 5

        move_mouse(130, 140, 110, 130) # move to first item in bank
        random_wait(.05, .2)
        click_object()
        pyautogui.press('escape')
        random_wait(.03, .08)
        pyautogui.press('f2')
        random_wait(.03, .08)
        pyautogui.press('f6')

        move_mouse(675, 683,590, 600)  # move to tan leather
        for i  in range(0,5):
            click_object()
            random_wait(1.8, 2.1)
        random_wait(.05, .2)

        move_mouse(425, 430, 470, 495)  # move to banker center screen
        random_wait(.05, .2)
        click_object()
        random_wait(.6, .75)

        move_mouse(650, 665,500, 510)  # move to first obj in inv (next box)
        random_wait(.05, .2)
        click_object()
        random_wait(.05, .2)

        t -= 1
        print(f'{t} actions remaining')
