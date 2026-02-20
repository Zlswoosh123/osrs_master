import re
from threading import Thread
import win32gui
import numpy as np
import cv2
import pyautogui
import random
import time
import argparse
import os
import yaml
import requests
import simplejson

from functions2 import TEAL_BGR

global hwnd
global iflag
global icoord
import datetime
import pytesseract
from PIL import Image, ImageGrab
from functions import Image_to_Text, findarea_attack_quick
from functions import resizeImage
from functions import image_Rec_clicker
from functions import Image_to_Text_combat, resizeImage_combat, offscreen_mouse
import functions
import core
import functions2 as f

BLUE_BGR = (255, 0, 0)
PINK_BGR = (255, 0, 255)
GREEN_BGR = (0, 255, 0)
PURPLE_BGR = (65, 4, 41)
RED_BGR = (0, 0, 255)
YELLOW_BGR = (0, 255, 255)

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

import re

import re

def extract_code(text):
    if not text:
        return None

    text = text.strip().replace('\n', ' ')

    # Less strict: capture after '(' up to ')' OR end of string
    m = re.search(r'\(\s*([^)]+)\s*(?:\)|$)', text)
    if not m:
        return None

    content = m.group(1).strip()

    # If OCR chopped the ')' we still have content like "ALA" or "done!"
    cleaned = re.sub(r'[^A-Za-z]', '', content).upper()

    # DONE case (done!, done, Done!, etc.)
    if cleaned.startswith("DONE"):
        return "DONE"

    # 3-letter code case (ALA, MLL, etc.)
    if len(cleaned) >= 3:
        # take first 3 letters in case OCR adds extra letters/noise
        return cleaned[:3]

    return None



def inv_count(name):
    return f.Image_count(name + '.png', threshold=0.8, left=0, top=0, right=810, bottom=750)

def see_order():
    f.screen_Image(left=43, top = 73, right=210, bottom=95, name='potion1.png')
    potion1 = f.Image_to_Text(preprocess='adaptive', image='potion1.png')
    p1_code = extract_code(potion1)

    f.screen_Image(left=43, top = 100, right=210, bottom=119, name='potion2.png')
    potion2 = f.Image_to_Text(preprocess='adaptive', image='potion2.png')
    p2_code = extract_code(potion2)

    f.screen_Image(left=43, top = 124, right=210, bottom=150, name='potion3.png')
    potion3 = f.Image_to_Text(preprocess='adaptive', image='potion3.png')
    p3_code = extract_code(potion3)

    print('Potion 1 is: ', potion1)
    print('p1_code is: ', p1_code)
    print('Potion 2 is: ', potion2)
    print('p2_code is: ', p2_code)
    print('Potion 3 is: ', potion3)
    print('p3_code is: ', p3_code)

    return p1_code, p2_code, p3_code

def create_potion(potion_code):
    check = f.click_color_bgr_in_region(target_bgr=PINK_BGR, region=(0, 180, 600, 635), click=False)[0]
    iter = 0
    retry = 0
    # new_count = inv
    print('Starting create_potion for:', potion_code,'. Check is: ', check)
    if not check:
        for p in potion_code:
            print('Starting create_potion for: ', potion_code, ' on ', p)
            # wait = random.uniform(.6, .7)
            if p == 'M' or p == 'W':
                f.click_color_bgr_in_region(target_bgr=BLUE_BGR, region=(0, 180, 600, 635))
            elif p == 'A' or p == 'R':
                f.click_color_bgr_in_region(target_bgr=GREEN_BGR, region=(0, 180, 600, 635))
            elif p == 'L' or p =='I' or p == 'U':
                f.click_color_bgr_in_region(target_bgr=RED_BGR, region=(0, 180, 600, 635), debug=True)
            else:
                print(f'Letter {p} not found no make potion! We have an issue')
                time.sleep(10000000)
                break
            if iter == 0:
                time.sleep(3.8)
            else:
                f.random_wait(.25,.5)
            iter +=1
        while retry <= 1 and not pink_check():
            print('Trying to create potion (purple). Retry:', retry)
            # print('new_count is: ', new_count, ' and inv is: ', inv)
            pyautogui.moveRel(0, 10)
            f.click_color_bgr_in_region(target_bgr=PURPLE_BGR, region=(0, 180, 600, 635))
            time.sleep(1.8)
            # new_count = inv_count('potion_unf')
            retry += 1
    else:
        pass

def process_potion():
    print('Starting process_potion, clicking pink')
    wait = random.randint(10,12)
    f.click_color_bgr_in_region(target_bgr=PINK_BGR, region=(0, 180, 600, 635))
    clock = time.time() + 16
    while pink_check() or color_check(f.ORANGE_BGR):
        if color_check(f.ORANGE_BGR):
            print('Teal found for special click')
            f.click_color_bgr_in_region(target_bgr=f.ORANGE_BGR, region=(0, 180, 600, 635))
            time.sleep(.6)
        if time.time() > clock:
            print('We may have misclicked pink, we waited 10s now trying again')
            f.click_color_bgr_in_region(target_bgr=PINK_BGR, region=(0, 180, 600, 635))
            clock = time.time() + 16

def deposit_potions():
    print('Starting deposit_potion, clicking yellow')
    wait = random.uniform(4,5.5)
    f.click_color_bgr_in_region(target_bgr=YELLOW_BGR, region=(0, 180, 600, 635))
    time.sleep(wait)

def pink_check():
    check = f.click_color_bgr_in_region(target_bgr=PINK_BGR, region=(0, 180, 600, 635),click=False)[0]
    if check:
        # print('Pink Found!')
        return True
    else:
        # print('Pink not found!')
        return False

def color_check(color=PINK_BGR, click = False):
    check = f.click_color_bgr_in_region(target_bgr=color, region=(0, 180, 600, 635),click=click)[0]
    if check:
        print(color, ' Found!')
        return True
    else:
        # print(color, ' not found!')
        return False

if __name__ == "__main__":
    print('Ensure this script is started zoomed very far out with black background for the text')
    # Colors (B, G, R)


    SEARCH_REGION = [0, 180, 600, 635]
    ACTIVE_BOUNDS = (SEARCH_REGION[0], SEARCH_REGION[1], SEARCH_REGION[2], SEARCH_REGION[3])

    Run_Duration_hours = 1
    t_end = time.time() + (60 * 60 * Run_Duration_hours)

    while time.time() < t_end:
        # count = f.inv_count('potion_unf', threshhold=.8)
        # print(count)
        p1, p2, p3 =  see_order()
        if p1 != 'DONE':
            create_potion(p1)
            if pink_check():
                process_potion()
        elif p2 != 'DONE':
            create_potion(p2)
            if pink_check():
                process_potion()
        elif p3 != 'DONE':
            create_potion(p3)
            if pink_check():
                process_potion()
        else:
            deposit_potions()

