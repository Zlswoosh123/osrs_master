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


def bar_check_green(name='gf_arrow_green'):
    return f.Image_count(name + '.png','gf_bar_green', threshold=0.8, left=165, top=80, right=222, bottom=105)


if __name__ == "__main__":
    # Colors (B, G, R)
    BLUE_BGR  = (255, 0, 0)
    PINK_BGR  = (240, 0, 255)
    GREEN_BGR = (0, 255, 0)
    PURPLE_BGR = (65, 4, 41)

    SEARCH_REGION = [0, 130, 600, 700]
    ACTIVE_BOUNDS = (SEARCH_REGION[0], SEARCH_REGION[1], SEARCH_REGION[2], SEARCH_REGION[3])

    Run_Duration_hours = 4.5
    t_end = time.time() + (60 * 60 * Run_Duration_hours)
    failsafe = 0
    local_check = time.time()
    while time.time() < t_end and failsafe < 5:
        print('Starting cycle!')
        wait = random.randint(5,25)
        # If name is found, look for pink color and click it
        name_check = f.onscreen_check('gemcrab_name.png')
        if name_check:
            print('found crab name')
            if time.time() > local_check:
                print('clicking crab')
                f.click_color_bgr_in_region(target_bgr=PINK_BGR)
                local_check = time.time() + random.randint(200,290)
            print('Waiting for: ', wait)
            time.sleep(wait)
            failsafe = 0
        else:
            print('Could not find grab, seeking blue. Failsafe is: ', failsafe)
            f.click_color_bgr_in_region(target_bgr=BLUE_BGR)
            local_check = time.time()
            time.sleep(random.randint(10,25))
            failsafe += 1