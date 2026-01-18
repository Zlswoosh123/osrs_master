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
    x_move = random.randrange(x1, x2)
    y_move = random.randrange(y1, y2)
    pyautogui.moveTo(x_move, y_move, duration=b)

def random_wait(a=.1, b=.3):
    c = random.uniform(a, b)
    time.sleep(c)



if __name__ == "__main__":
    t = (150//27) + 1
    flag = True # Determines if a second chisel is applied to gem to make tips
    while t > 0:
        # move_mouse(125, 140, 120,130) # move to first item in bank
        # random_wait(.05, .2)
        # click_object()
        # random_wait(.05, .1)

        move_mouse(175, 190, 120, 130) # move to 2nd item in bank
        random_wait(.05, .2)
        click_object()
        pyautogui.press('escape')
        random_wait(.05, .1)

        move_mouse(650, 665,500, 515)  # move to first obj in inv (next box)
        random_wait(.05, .2)
        click_object()
        random_wait(.05, .2)

        move_mouse(695, 710, 500, 515)  # move to 2nd obj in inv (nests)
        random_wait(.05, .2)
        click_object()
        random_wait(1, 1.2)
        pyautogui.press('space')
        random_wait(33, 41)

        if flag == True:
            move_mouse(650, 665,500, 515)  # move to first obj in inv (next box)
            random_wait(.05, .2)
            click_object()
            random_wait(.05, .2)

            move_mouse(695, 710, 500, 515)  # move to 2nd obj in inv (nests)
            random_wait(.05, .2)
            click_object()
            random_wait(1, 1.2)
            pyautogui.press('space')
            random_wait(80, 88)

        move_mouse(425, 430, 370, 390)  # move to banker center screen
        random_wait(.05, .2)
        click_object()
        random_wait(.6, .75)

        move_mouse(480, 490, 625, 635)  # empty all
        random_wait(.05, .2)
        click_object()
        random_wait(.05, .2)
        t -= 1
        print(f'{t} actions remaining')
