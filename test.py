from threading import Thread

import pyautogui
import pywintypes
import win32con
import win32gui
import win32api
import numpy as np
import cv2
import pyautogui as p
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
from functions import safe_open, find_and_click

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
        # print(f'image before mask is {image}')
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
        # print(whalf, hhalf)
        # print(x, y)
        x = random.randrange(x + 5, x + max(whalf - 5, 6)) + left # 950,960
        y = random.randrange(y + 5, y + max(hhalf - 5, 6)) + top# 490,500
        return (x, y)
    else:
        print('No contours!')
        return (None, None)
red = ([0, 0, 180], [80, 80, 255])  # 0 Index
green = ([0, 180, 0], [80, 255, 80])  # 1 Index
amber = ([0, 200, 200], [60, 255, 255])  # 2 Index
pickup_high = ([250, 0, 167], [255, 5, 172])  # 3 Index
attack_blue = ([250, 250, 0], [255, 255, 5])
purple = [([192, 0, 192], [255, 64, 255])]

def bootup_seq():
    absorb_count = 0
    overload_count = 0
    while absorb_count != 19 and overload_count != 7:
        print('Starting resource loop')
        # CHEST SECTIONS HERE
        # Store absorb potions
        print('Storing abs pots')
        x, y = find_object(boundaries=[([0, 180, 0], [80, 255, 80])])
        functions.move_mouse(x, x + 1, y, y + 1, click=True, type='right')
        p.moveRel(0, 60)
        p.click()
        time.sleep(6)
        p.press('1')
        time.sleep(1)
        # Store overload potions
        print('Storing ovl pots')
        x, y = find_object(boundaries=[([0, 200, 200], [60, 255, 255])])
        functions.move_mouse(x, x + 1, y, y + 1, click=True, type='right')
        time.sleep(2)
        p.moveRel(0, 60)
        p.click()
        time.sleep(6)
        p.press('1')
        time.sleep(1)

        # Click chest
        print('Clicking chest')
        x, y = find_object(boundaries=[([0, 0, 180], [80, 80, 255])])
        functions.move_mouse(x + 5, x + 20, y + 10, y + 25, click=True, type='right')
        time.sleep(1)
        p.moveRel(0, 28)
        # functions.find_and_click(object='search_rewards_chest.png', xadd = 25, yadd= 2,)
        p.click()
        time.sleep(6)

        # inside the chest
        benes = functions.find_and_click(object='benefits.png')
        print('Benes is', benes)
        time.sleep(1)
        # Buying absorbs
        functions.find_and_click(object='absorb_shop.png', clicker='right')
        p.moveRel(0, 90)
        p.click()
        time.sleep(1)
        p.write('999')
        p.press('enter')
        # Buying overloads
        functions.find_and_click(object='overload_shop.png', clicker='right')
        p.moveRel(0, 90)
        p.click()
        time.sleep(1)
        p.write('999')
        p.press('enter')
        time.sleep(1)
        p.press('esc')

        # OVERLOAD POTIONS HERE
        # # Store overload potions
        # x, y = find_object(boundaries=[([0, 200, 200], [60, 255, 255])])
        # functions.move_mouse(x, x + 1, y, y + 1, click=True, type='right')
        # time.sleep(2)
        # p.moveRel(0, 60)
        # p.click()
        # time.sleep(6)
        # p.press('1')
        # time.sleep(1)
        print('Adding ovls to inv')
        x, y = find_object(boundaries=[([0, 200, 200], [60, 255, 255])])
        functions.move_mouse(x+2, x + 5, y+3, y + 5, click=True, type='right')
        p.moveRel(0, 40)
        p.click()
        time.sleep(7)
        p.write('28')  # Take  potions
        p.press('enter')
        time.sleep(2)

        # ABSORB POTIONS HERE
        # # Store absorb potions
        # x, y = find_object(boundaries=[([0, 180, 0], [80, 255, 80])])
        # functions.move_mouse(x, x+1, y, y+1, click=True, type='right')
        # p.moveRel(0, 60)
        # p.click()
        # time.sleep(6)
        # p.press('1')
        # time.sleep(1)
        print('Adding Absorbs to inv')
        x, y = find_object(boundaries=[([0, 180, 0], [80, 255, 80])])
        functions.move_mouse(x, x + 1, y, y + 1, click=True, type='right')
        p.moveRel(0, 40)
        p.click()
        time.sleep(2)
        p.write('76')  # Take abs potions
        p.press('enter')
        time.sleep(1)

        absorb_count = functions.invent_count('absorb4.png', threshold=.9518)
        overload_count = functions.invent_count('overload4.png', threshold=.951)
        print('Potion Counts: ', overload_count, absorb_count)
    entry_flag = False
    while entry_flag == False:
        print('Starting dreamer loop')
        # Find dream NPC boundaries=[([110, 100, 0], [195, 180, 60])]
        print('Finding Dreamer')
        x, y = find_object(boundaries=[([128, 128, 0], [255, 255, 128])])
        functions.move_mouse(x + 5, x + 10, y + 5, y + 10, click=True, type='right')
        p.moveRel(0, 40)
        p.click()
        time.sleep(5)
        p.write('4')
        time.sleep(2)
        p.press('space')
        time.sleep(1)
        p.write('1')
        time.sleep(1)
        p.press('space')

        # Start the dream
        print('Starting Dream!')
        x, y = find_object(boundaries=[([192, 0, 192], [255, 64, 255])])
        if x is not None and y is not None:
            functions.move_mouse(x - 8, x - 7, y + 1, y + 2, click=True, type='left')
        time.sleep(3)

        accept = find_and_click(object='accept.png')
        print('Accept is: ', accept)
        time.sleep(5)

        if accept:
            # Run to tile
            x, y = find_object(boundaries=[([0, 200, 200], [60, 255, 255])])
            functions.move_mouse(x, x + 1, y, y + 1, click=True, type='left')
            time.sleep(5)
            pyautogui.press('esc')
            # entry_flag = find_and_click(object='points.png', clicker='right')
            print('Entry_flag is now: ', entry_flag)
            entry_flag= True
            print('Ending Boot seq')
            return
            # time.sleep(3)
            # entry_flag = find_and_click(object='points.png', clicker='right')
# if __name__ == "__main__":
    # bootup_seq()
