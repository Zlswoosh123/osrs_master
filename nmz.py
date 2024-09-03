from functions import move_mouse
import datetime as dt
import random as r
import time
import pyautogui
import win32gui
import core
import yaml
global hwnd
global iflag
global icoord
iflag = False
global newTime_break
newTime_break = False
global timer
global timer_break
global ibreak

inventory_spots = [
    (650, 660, 498, 505),  # Spot 1
    (693, 703, 498, 505),  # Spot 2
    (736, 746, 498, 505),  # Spot 3
    (779, 789, 498, 505),  # Spot 4
    (650, 660, 533, 540),  # Spot 5
    (693, 703, 533, 540),  # Spot 6
    (736, 746, 533, 540),  # Spot 7
    (779, 789, 533, 540),  # Spot 8
    (650, 660, 568, 575),  # Spot 9
    (693, 703, 568, 575),  # Spot 10
    (736, 746, 568, 575),  # Spot 11
    (779, 789, 568, 575),  # Spot 12
    (650, 660, 603, 610),  # Spot 13
    (693, 703, 603, 610),  # Spot 14
    (736, 746, 603, 610),  # Spot 15
    (779, 789, 603, 610),  # Spot 16
    (650, 660, 638, 645),  # Spot 17
    (693, 703, 638, 645),  # Spot 18
    (736, 746, 638, 645),  # Spot 19
    (779, 789, 638, 645),  # Spot 20
    (650, 660, 673, 680),  # Spot 21
    (693, 703, 673, 680),  # Spot 22
    (736, 746, 673, 680),  # Spot 23
    (779, 789, 673, 680),  # Spot 24
    (650, 660, 708, 715),  # Spot 25
    (693, 703, 708, 715),  # Spot 26
    (736, 746, 708, 715),  # Spot 27
    (779, 789, 708, 715),  # Spot 28
]


def click_heal():
    print('Heal start')
    pyautogui.press('f1')
    pyautogui.press('f5')
    time.sleep(.1)
    move_mouse(782,795, 535, 545, True)
    print('Heal end')

def click_abs(abs_counter):
    print('Abs start')
    pyautogui.press('f1')
    pyautogui.press('esc')
    row = (abs_counter * 4) + 8
    for i in range(row, row+4):
        move_mouse(*inventory_spots[i], True)
    print('Abs end')


def click_buff(repot_counter):
    print('Buff start')
    pyautogui.press('f1')
    pyautogui.press('esc')
    temp  = (repot_counter // 4) + 1# says which inventory spot to click
    move_mouse(*inventory_spots[temp], True)
    print('Buff end')


def click_cake(times=28):
    print('Cake start')
    pyautogui.press('f1')
    pyautogui.press('esc')
    for i in range(times):
        move_mouse(*inventory_spots[0], False)
        pyautogui.click(button='right')
        pyautogui.move(0,37)
        pyautogui.click()
        time.sleep(.05)
    print('Cake end')

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





# end = time.now() + 10800
end = dt.datetime.now() + dt.timedelta(hours=3)
now = dt.datetime.now()
repot = dt.datetime.now() + dt.timedelta(seconds=303)
abs = dt.datetime.now() + dt.timedelta(seconds=90)
heal = dt.datetime.now() + dt.timedelta(seconds=35)
log = dt.datetime.now() + dt.timedelta(seconds=15)

cake = True
counter = 0
repot_counter = 0
abs_counter = 0
abs_flag = False
while now < end:
    if cake == True and counter == 0:
        click_buff(repot_counter)
        time.sleep(5)
        click_cake(22)
        repot_counter += 1
        for i in range(5):
            click_abs(abs_counter)
            abs_counter += 1
        click_cake(2)
        abs_counter = 0
    if repot < now:
        repot = dt.datetime.now() + dt.timedelta(seconds=303)
        for i in range(2):
            click_buff(repot_counter)
        time.sleep(7)
        click_heal()
        time.sleep(1)
        click_heal()
        time.sleep(1)
        click_cake(2)
        repot_counter += 1
        abs_flag = True
    if abs < now or abs_flag == True:
        abs = dt.datetime.now() + dt.timedelta(seconds=90)
        click_abs(abs_counter)
        abs_counter += 1
        if abs_counter >= 5:
            abs_counter = 0
        abs_flag = False
    if log < now:
        print(f'Time until repot = {repot - now}')
        print(f'Time until abs = {abs - now}')
        print(f'Time until heal = {heal - now}')
        log = dt.datetime.now() + dt.timedelta(seconds=15)
    if heal < now:
        sleep = r.randint(30, 45)
        click_heal()
        time.sleep(.05)
        click_heal()
        heal = dt.datetime.now() + dt.timedelta(seconds=sleep)
    now = dt.datetime.now()

    counter += 1
