from threading import Thread

import pywintypes
import win32gui
import numpy as np
import cv2
import pyautogui
import random
import time
import os
import functions
import pytesseract
import core
import yaml
from functions import Image_to_Text, invent_crop, resizeImage,random_breaks, image_eel_clicker,screen_front
import functions2 as f2
import runtime_vars as v

# Vars
runelite = functions.runelite

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

def banking():
    print('Banking start')
    # pyautogui.press('space')
    time.sleep(1)
    failsafe = 0
    f2.click_color_bgr_in_region(target_bgr=f2.PINK_BGR)
    if f2.click_color_bgr_in_region(target_bgr=f2.PINK_BGR, click=False)[0]:
        f2.open_inventory_menu()
    pyautogui.moveTo(300,300)
    while f2.icon_check() < 1 and failsafe < 20:
        time.sleep(1)
        failsafe += 1
    if failsafe >= 19:
        f2.click_color_bgr_in_region(target_bgr=f2.PINK_BGR)
        time.sleep(7)
    time.sleep(.7)
    if f2.icon_check():
        f2.move_mouse(*f2.special_spots['empty'], click=True)  # empty all
        f2.random_wait(.7, 1.5)
        if v.fish_barrel:
            f2.move_mouse(*f2.inventory_spots[0], click=True)
            time.sleep(1)
    pyautogui.press('escape')

def manage_fish(action = v.fishing_action):  # type can be 'drop', 'eel' (hammer fish), or bank
    print('manage_fish start')
    if action == 'drop':
        f2.drop_loot(exclude=v.exclude)
    if action == 'eel':
        f2.move_mouse(*f2.inventory_spots[0], click=True)
        time.sleep(.2)
        f2.move_mouse(*f2.inventory_spots[1], click=True)
        time.sleep(5)  # todo fix wait time for this
    if action == 'bank':
        while not f2.click_color_bgr_in_region(target_bgr=f2.PINK_BGR, click = False)[0]:
            pyautogui.press('space')
            time.sleep(1)
            f2.open_inventory_menu()
            time.sleep(1)
            f2.move_mouse(*f2.inventory_spots[27], click=True)  # tele to bank
            time.sleep(7)
        banking()
        time.sleep(1)
        f2.move_mouse(*f2.inventory_spots[26], click=True)  # tele to fairy ring
        time.sleep(7.5)
        while not f2.click_color_bgr_in_region(target_bgr=f2.DARK_PINK, click=False)[0]:
            f2.click_color_bgr_in_region(target_bgr=f2.PINK_BGR)
            time.sleep(7.5)


def find_fish():
    print('find_fish start')
    f2.click_color_bgr_in_region(f2.DARK_PINK, click=True)
    time.sleep(12)

fishing_text = 'Not Fishing'
Run_Duration_hours = v.run_duration_hours
t_end = time.time() + (60 * 60 * Run_Duration_hours)
print('If banking, ensure fish barrel is in inv slot 1, quest cape in 27, bank tele in in slot 28')
print('Fish and fishing vessel in slots 1/2. All locked to ensure clean banking')
if __name__ == "__main__":
    while time.time() < t_end:
        empty_count = f2.Image_count('empty_slot.png')
        print('empty count is: ', empty_count)
        f2.screen_Image(18, 48, 142, 71, 'fishing_action.png')
        if empty_count == 0:
            f2.open_inventory_menu()
            time.sleep(.6)
            empty_count = f2.Image_count('empty_slot.png')

        fishing_text = f2.Image_to_Text('thresh', 'fishing_action.png')
        print('fishing text is: ', fishing_text)
        if fishing_text.strip().lower().replace(",", "") not in ('fishing', 'fishin'):
            find_fish()
        if empty_count == 0:
            if v.fish_barrel:
                f2.move_mouse(*f2.inventory_spots[0], click=True)
                time.sleep(1)
                empty_count = f2.Image_count('empty_slot.png')
            if empty_count == 0:
                manage_fish()


