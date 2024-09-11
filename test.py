from threading import Thread
import pywintypes
import win32con
import win32gui
import win32api
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
from PIL import Image
from functions import Image_count
from functions import image_Rec_clicker
from functions import screen_Image
from functions import release_drop_item
from functions import drop_item
from functions import Image_to_Text
from functions import invent_crop
from functions import resizeImage
from functions import random_breaks
from functions import image_eel_clicker
from functions import screen_front
from functions import offscreen_mouse
from functions import super_random_breaks
from functions import safe_open

def find_object(showCoords=False, left=0, right=800, top=0, bottom=800, boundaries=[([0, 0, 180], [80, 80, 255])]):
    global window
    functions.screen_Image(left, right, top, bottom)
    image = cv2.imread('images/screenshot.png')
    safe_open(image, 'screenshot.png')
    image = cv2.rectangle(image, pt1=(600, 0), pt2=(850, 200), color=(0, 0, 0), thickness=-1)
    image = cv2.rectangle(image, pt1=(0, 0), pt2=(150, 100), color=(0, 0, 0), thickness=-1)

    # loop over the boundaries
    for (lower, upper) in boundaries:
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")
        safe_open(image, 'screenshot.png')
        # find the colors within the specified boundaries and apply the mask
        print(f'image before mask is {image}')
        contours = ""
        if image is not None:
            mask = cv2.inRange(image, lower, upper)
            ret, thresh = cv2.threshold(mask, 40, 255, 0)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            # cv2.imshow('Mask', mask)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
    if len(contours) != 0:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        if showCoords:
            print(x, y, w, h)
        whalf = max(round(w / 2), 1)
        hhalf = max(round(h / 2), 1)
        print(whalf, hhalf)
        print(x, y)
        x = random.randrange(x + 5, x + max(whalf - 5, 6)) + left # 950,960
        y = random.randrange(y + 5, y + max(hhalf - 5, 6)) + top# 490,500
        return (x, y)
    else:
        print('No contours!')
        return False
red = ([0, 0, 180], [80, 80, 255])  # 0 Index
green = ([0, 180, 0], [80, 255, 80])  # 1 Index
amber = ([0, 200, 200], [60, 255, 255])  # 2 Index
pickup_high = ([250, 0, 167], [255, 5, 172])  # 3 Index
attack_blue = ([250, 250, 0], [255, 255, 5])

def bootup_seq():
    # click chest
    left_ss, top_ss, right_ss, bottom_ss = 0, 800, 0, 800
    x, y = find_object(boundaries=[([0, 0, 180], [80, 80, 255])])
    functions.move_mouse(x, x+1, y, y+1, click=True)
    time.sleep(8)
    pyautogui.press('esc')

    # click abs
    x, y = find_object(boundaries=[([0, 180, 0], [80, 255, 80])])
    functions.move_mouse(x, x+1, y, y+1, click=True)
    time.sleep(8)

    # click ovl
    x, y = find_object(boundaries=[([0, 200, 200], [60, 255, 255])])
    functions.move_mouse(x, x+1, y, y+1, click=True)
    time.sleep(8)