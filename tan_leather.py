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

# Boundaries are color boundaries
def find_banker(showCoords=False, left=0, top=0, right=800, bottom=800, boundaries=[([110, 100, 0], [195, 180, 60])]):
    global window
    functions.screen_Image(left, top, right, bottom)
    image = cv2.imread('images/screenshot.png')
    safe_open(image, 'screenshot.png')
    # image = cv2.rectangle(image, pt1=(600, 0), pt2=(850, 200), color=(0, 0, 0), thickness=-1)
    # image = cv2.rectangle(image, pt1=(0, 0), pt2=(150, 100), color=(0, 0, 0), thickness=-1)

    # loop over the boundaries
    for (lower, upper) in boundaries:
        # create NumPy arrays from the boundaries
        lower, upper = np.array(lower, dtype="uint8"), np.array(upper, dtype="uint8")
        safe_open(image, 'screenshot.png')
        # print(f'image before mask is {image}')
        contours = ""
        # find the colors within the specified boundaries and apply the mask
        # Pixels below 40 turn black, rest turn white (255). 0 is type of op, ignore
        if image is not None:
            mask = cv2.inRange(image, lower, upper)
            ret, thresh = cv2.threshold(mask, 40, 255, 0)
            # External: specifies that only external contours are detected (those that form the boundary of an object).
            # Approx_none: specifies that all contour points are stored, without any compression or approximation.
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        if showCoords:
            print(x, y, w, h)
        x = random.randrange(x + 5, x + max(w - 5, 6)) + left  # 950,960
        y = random.randrange(y + 5, y + max(h - 5, 6)) + top  # 490,500
        b = random.uniform(0.2, 0.4)
        pyautogui.moveTo(x, y, duration=b)
        b = random.uniform(0.01, 0.05)
        pyautogui.click(duration=b)
        return (x, y)
    else:
        return False
def pick_banker(top_ss=0, left_ss=0, right_ss=800, bottom_ss=800, showCoords=False):
    left_ss, top_ss, right_ss, bottom_ss = 0, 0, 800, 800
    banker = find_banker(False, left_ss, top_ss, right_ss, bottom_ss)
    return banker

def tan_leather(monster='Banker', take_human_break=True, Run_Duration_hours=3):
    print('Starting tan_leather which should click spell')
    global actions
    global runelite
    actions = "Making eel sushi - always hot but never seared"
    invent_crop()
    double_random(1, 2) # safety wait, possibly remove
    # Open Bank
    coords = functions.findarea_attack_quick(3)
    if coords[0] != 0:  # attack npc/monster
        c = double_random(2,4)
        print(f'coords[0] is: {coords[0]} and coords[1] is {coords[1]}')
        time.sleep(c)
        if take_human_break:
            c = random.triangular(0.1, 50, 3)
            time.sleep(c)
    print('Ending powerattack_text')
    # Withdraw Hides

    # Close Bank

    # Open Magic menu

    # Move mouse and click spell x5 (check tick delay)

    # Move to tan leather spell
    # move_wait = double_random(.1, .22)
    # pyautogui.moveTo(hammer_coord, duration=move_wait)
    # click_wait = double_random(.1, .22)
    # print('Trying to click coord!')
    # screen_front(runelite)
    # pyautogui.click(hammer_coord, duration=click_wait, button='left')
    #
    # image_eel_clicker(r'infernal_eel.png', 'Clicking Eel', 2, 2, 0.95, 'left', 10, False, True)

def timer_countdown():
    global Run_Duration_hours
    global timer_log
    global inv_cap
    t_end = time.time() + (60 * 60 * Run_Duration_hours)
    #print(t_end)
    final = round((60 * 60 * Run_Duration_hours) / 1)
    #print(final)
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

def test(monster='Banker', burybones=False, Pickup_loot=False, Take_Human_Break=False,
                         Run_Duration_hours=6):
    print('Starting powerattack_text!')
    global coords, combat_text, time_left, powerlist, actions, powerlist, t_end
    t1 = Thread(target=timer_countdown)
    t1.start()
    t_end = time.time() + (60 * 60 * Run_Duration_hours)
    monster_list = ['Banker', 'chicken', 'guard', 'cow', 'monk', 'imp', 'skeleton', 'dwarf', 'giant frog', 'goblin']
    monster_array = [['Banker'], ['chicken'], ['guard', 'gua rd'], ['cow', 'cou'], ['monk'], ['imp'], ['skeleton'], ['dwarf'],
                     ['giant frog', 'giant', 'frog'], ['goblin']]
    group = monster_list.index(monster)
    while time.time() < t_end:
        print('Start of while loop')
        r = random.uniform(0.1, 5)
        functions.resizeImage_combat()
        # combat_text = functions.Image_to_Text_combat('thresh', 'screen_resize.png')
        attack = 0
        for monsters in monster_array[group]:
            print(f'Current monster is: {monster}')
            print(combat_text.strip().lower().find(monsters))
            if combat_text.strip().lower().find(monsters) == -1:
                attack += 1
        if attack == len(monster_array[group]):
            d = random.uniform(0.05, 0.1)
            time.sleep(d)
            coords = findarea_attack_quick(3)
            off = random.randint(0, 5)
            if off == 3:
                offscreen_mouse()
            if coords[0] != 0:  # attack npc/monster
                c = random.uniform(2, 4)
                print(f'coords[0] is: {coords[0]} and coords[1] is {coords[1]}')
                time.sleep(c)
                if Take_Human_Break:
                    c = random.triangular(0.1, 50, 3)
                    time.sleep(c)
            print('Ending test')

if __name__ == "__main__":
    test(monster='Banker', burybones=False, Pickup_loot=False, Take_Human_Break=False,
         Run_Duration_hours=6)
    # print(f'window is {window}')
    # xrand = 0
    # yrand = 0
    # xrand, yrand = rand_click(xrand, yrand)
    # print(f'xrand is {xrand}')
    # print(f'yrand is {yrand}')
    # time.sleep(1)
    # resizeImage()
    # invent_crop()
    # x = xrand
    # print(f'Right click x cord is: {x}')
    # y = yrand
    # print(f'Right click y cord is: {y}')
    # pyautogui.click(x, y, button='right')
    # ibreak = random.randrange(300, 2000)
    # # timer_break = timer()
    # # --------- CHANGE TO RUN FOR AMOUNT OF HOURS ----------------
    # Run_Duration_hours = 5.1

