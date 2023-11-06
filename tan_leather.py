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
from functions import Image_to_Text
from functions import random_breaks
from functions import invent_crop
from functions import resizeImage
from functions import random_combat
from functions import random_quests
from functions import random_skills
from functions import random_inventory
from functions import random_breaks
from functions import image_eel_clicker
from functions import screen_front
from functions import offscreen_mouse
from functions import super_random_breaks
from functions import safe_open
from functions import double_random
from functions import findarea_attack_quick

# Variables
global hwnd
global iflag
global icoord
iflag = False
global newTime_break
newTime_break = False
global timer
global timer_break
global ibreak
Run_Duration_hours = 5
timer_log = 0
runelite = functions.runelite
inv_cap = random.randint(14, 17) # init inv cap to read in status
window = functions.window
print(f'Window is {window}')
iflag = False
global top, left, right, bottom
# options = {0: random_inventory,
#            1: random_combat,
#            2: random_skills,
#            3: random_quests,
#            4: random_pause}

class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR

# Funcs
def gfindWindow(data):  # find window name returns PID of the window
    global hwnd
    global window
    hwnd = win32gui.FindWindow(None, data)
    win32gui.SetActiveWindow(hwnd)
    win = win32gui.GetForegroundWindow()
    win32gui.MoveWindow(hwnd, 0, 0, 865, 830, True)

    # window 1: (hwnd, 0, 0, 865, 830, True)
    # window 2: (hwnd, 875, 0, 1000, 830, True)

with open("pybot-config.yaml", "r") as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)

try:
    gfindWindow(data[0]['Config']['client_title'])
except BaseException:
    print("Unable to find window:", data[0]['Config']['client_title'], "| Please see list of window names below:")
    core.printWindows()
    print(BaseException)
    pass

try:
    x_win, y_win, w_win, h_win = core.getWindow(data[0]['Config']['client_title'])
except BaseException:
    print("Unable to find window:", data[0]['Config']['client_title'], "| Please see list of window names below:")
    core.printWindows()
    print(BaseException)
    pass

def timer_countdown():
    global Run_Duration_hours
    global timer_log
    global inv_cap
    t_end = time.time() + (60 * 60 * Run_Duration_hours)
    # print(t_end)
    final = round((60 * 60 * Run_Duration_hours) / 1)
    # print(final)
    for i in range(final):
        # the exact output you're looking for:
        if timer_log % 10 == 0:
            timer_log += 1
            time.sleep(1)
        if timer_log % 10 == 0:
            functions.screen_Image(0, 0, 800, 800)


def rand_click(xrand, yrand):
    xrand = random.randrange(100, 450)
    yrand = random.randrange(250, 600)
    return xrand, yrand

def tan_leather(monster='Banker', Run_Duration_hours=3):
    print('Starting tan_leather which should click spell')
    global actions
    global runelite
    t_end = time.time() + (60 * 60 * Run_Duration_hours)
    while time.time() < t_end:
        invent_crop()
        functions.screen_Image(0, 0, 800, 800, 'screenshot.png')
        double_random(1, 2) # safety wait, possibly remove
        # Open Bank and deposit hides
        open_bank()
        # Withdraw Hides
        withdraw_item(112, 115, -7, 10, 123, 130, -7, 9)
        # Close Bank
        wait = super_random_breaks(.1, .25, 1, 1.5)
        time.sleep(wait)
        pyautogui.press('esc')
        # Open Magic menu
        pyautogui.press('F6')
        wait = super_random_breaks(.1, .25, 1, 1.5)
        time.sleep(wait)
        # Move mouse and click spell x5 (check tick delay)
        cast_spell()
        # Open bank
        open_bank()
        # Deposit hides
        withdraw_item(645, 651, -7, 10, 557, 568, -7, 9)

def open_bank(monster='Banker'):
    print('Starting powerattack_text!')
    global coords
    monster_list = ['Banker']
    monster_array = [['Banker']]
    group = monster_list.index(monster)
    functions.resizeImage_combat()
    attack = 0
    attack += 1
    if attack == len(monster_array[group]):
        time.sleep(random.uniform(.05, .15))
        coords = findarea_attack_quick(3)
    time.sleep(double_random(2,4))

def withdraw_item(x1, x2, xrand1, xrand2, y1, y2, yrand1, yrand2):
    xitem = random.randint(x1, x2) + random.randint(xrand1, xrand2)  # 101-131 limit for top-left bank
    yitem = random.randint(y1, y2) + random.randint(yrand1, yrand2)  # 113 - 143 limit for top-left bank
    item_coord = (xitem, yitem)
    speed = super_random_breaks(.08, .2, .3, .4)
    pyautogui.moveTo(item_coord, duration=speed)
    speed = super_random_breaks(.03, .12, .14, .25)
    print('Trying to click coord!')
    screen_front(runelite)
    pyautogui.click(item_coord, duration=speed, button='left')

def cast_spell():
    count = 0
    xspell = random.randint(670, 673) + random.randint(-7, 10)  # 661-685 limit for tan leather
    yspell = random.randint(586, 590) + random.randint(-7, 9)  # 577 - 602
    spell_coord = (xspell, yspell)
    speed = super_random_breaks(.08, .2, .3, .4)
    pyautogui.moveTo(spell_coord, duration=speed)
    speed = super_random_breaks(.03, .12, .14, .25)
    screen_front(runelite)
    while count <= 4:
        pyautogui.click(spell_coord, duration=speed, button='left')
        time.sleep(random.uniform(1.5, 2.5))
        count += 1

if __name__ == "__main__":
    print(f'window is {window}')
    xrand = 0
    yrand = 0
    xrand, yrand = rand_click(xrand, yrand)
    print(f'xrand is {xrand}')
    print(f'yrand is {yrand}')
    time.sleep(1)
    resizeImage()
    invent_crop()
    x = xrand
    print(f'Right click x cord is: {x}')
    y = yrand
    print(f'Right click y cord is: {y}')
    pyautogui.click(x, y, button='right')
    # --------- CHANGE TO RUN FOR AMOUNT OF HOURS ----------------
    Run_Duration_hours = 5.1
    tan_leather()


