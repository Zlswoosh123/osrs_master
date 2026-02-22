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
import runtime_vars as v

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


def inv_count(name):
    return f.Image_count(name + '.png', threshold=0.8, left=0, top=0, right=810, bottom=750)

def restock():
    wait = random.randint(2,5)
    f.click_color_bgr_in_region(target_bgr=PINK_BGR)
    time.sleep(wait)
    functions.move_mouse(125, 140, 120, 130)  # move to first item in bank (grab mithril)
    f.random_wait(.15, .3)
    functions.click_object()
    f.random_wait(.15, .3)
    pyautogui.press('escape')
    time.sleep(.6)

if __name__ == "__main__":
    print('Ensure that the bank tile is pink and deposit tile is blue before starting!')
    # Colors (B, G, R)
    BLUE_BGR  = (255, 0, 0)
    PINK_BGR  = (240, 0, 255)
    GREEN_BGR = (0, 255, 0)
    PURPLE_BGR = (65, 4, 41)

    SEARCH_REGION = [0, 130, 600, 700]
    ACTIVE_BOUNDS = (SEARCH_REGION[0], SEARCH_REGION[1], SEARCH_REGION[2], SEARCH_REGION[3])

    Run_Duration_hours = v.run_duration_hours
    t_end = time.time() + (60 * 60 * Run_Duration_hours)
    failsafe = 0
    local_check = time.time()
    lap = 0
    max_lap = v.amount_to_do_mm_herb // 27
    print('Ending after ', max_lap, ' laps')
    while time.time() < t_end and lap <= max_lap:
        print('Starting cycle!')

        # If name is found, look for pink color and click it
        count = inv_count('herb')
        count2 = inv_count('herb2')

        while count > 0 or count2 > 0:
            wait = random.uniform(.05, .25)
            f.click_color_bgr_in_region(target_bgr=BLUE_BGR)
            time.sleep(wait)
            print(count)
            count = inv_count('herb')
            count2 = inv_count('herb2')

        restock()
        lap += 1
        print('Now on lap ',lap, ' of ', max_lap)

