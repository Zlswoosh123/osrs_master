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
from functions_bkp import Image_to_Text
from functions_bkp import invent_crop
from functions_bkp import resizeImage
from functions import random_breaks
from functions import image_eel_clicker
from functions import screen_front
from functions import offscreen_mouse
from functions import super_random_breaks
from functions import safe_open

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
timer_log = 0
runelite = functions.runelite
inv_cap = random.randint(14, 16) # init inv cap to read in status
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
def random_break(start, c):
    global newTime_break
    startTime = time.time()
    # 1200 = 20 minutes
    a = random.randrange(0, 4)
    # if startTime - start > c:
    #     options[a]()
    #     newTime_break = True


def randomizer(timer_breaks, ibreaks):
    global newTime_break
    global timer_break
    global ibreak
    random_break(timer_breaks, ibreaks)
    if newTime_break == True:
        timer_break = timer()
        ibreak = random.randrange(600, 2000)
        newTime_break = False

    # b = random.uniform(4, 5)


def timer():
    startTime = time.time()
    return startTime


def random_pause():
    b = random.uniform(20, 250)
    print('pausing for ' + str(b) + ' seconds')
    time.sleep(b)
    newTime_break = True

def drop_fish():
    print('Starting drop_fish which should click hammer and eel!')
    global actions
    global runelite
    actions = "Making eel sushi - always hot but never seared"
    invent_crop()

    # Setting random timer vars
    c = random.uniform(0.1, 0.2)
    d = random.uniform(0.1, 0.23)
    e = random.uniform(0.1, 0.3)
    f = random.uniform(0.1, 0.2)
    time.sleep(c)

    # Get runelite window
    screen_front(runelite)
    time.sleep(d)
    # Drop click items
    if fish_type == 'infernal_eel':
        hammer = functions.invent_count('hammer.png', .7)
        xham= random.randint(655,660) + random.randint(0, 10) # 648, 670
        yham= random.randint(505,515) + random.randint(0,5) # 500, 520
        hammer_coord =(xham, yham)
        b = super_random_breaks(.03, .12, .14, .25)
        # b = random.uniform(0.05, 0.15)
        pyautogui.moveTo(hammer_coord, duration=b)
        b = super_random_breaks(.03, .12, .14, .25)
        # b = random.uniform(0.05, 0.15)
        print('Trying to click coord!')
        screen_front(runelite)
        pyautogui.click(hammer_coord, duration=b, button='left')


        print(f'Hammer count is {hammer}')
        image_eel_clicker(r'hammer.png', 'Clicking hammer', 2, 2, 0.7, 'left', 10, False, True)

        time.sleep(random.uniform(.3, .8))
        image_eel_clicker(r'infernal_eel.png', 'Clicking Eel', 2, 2, 0.95, 'left', 10, False, True)
        # image_eel_clicker(r'infernal_eel2.png', 'Clicking Eel', 5, 5, 0.7, 'left', 10, False, True)
        eel_wait = functions.invent_count(fish_type + '.png', .95) * 3 * .6
        sleep = min(40, int(random.uniform(eel_wait + 1, eel_wait + 10)))
        print(f'Waiting for {sleep}s while eels breakdown')
        time.sleep(sleep)
    else:
        image_Rec_clicker(r'prawn_fish.png', 'dropping item', 5, 5, 0.9, 'left', 10, False, fast=True)
        image_Rec_clicker(r'trout_fish.png', 'dropping item', 5, 5, 0.9, 'left', 10, False, fast=True)
        image_Rec_clicker(r'trout_fish2.png', 'dropping item', 5, 5, 0.9, 'left', 10, False, fast=True)
        # image_Rec_clicker(r'salmon_fish.png', 'dropping item', 5, 5, 0.9, 'left', 10, False, False)
        # image_Rec_clicker(r'lobster_fish.png', 'dropping item', 5, 5, 0.9, 'left', 10, False, False)
        actions = "all fish dropped"
    time.sleep(f)


def find_fish(showCoords=False, left=0, top=0, right=800, bottom=800, boundaries=[([110, 100, 0], [195, 180, 60])]):
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
            print('Image is not none')
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
        x = random.randrange(x + 5, x + max(whalf - 5, 6)) + left # 950,960
        y = random.randrange(y + 5, y + max(hhalf - 5, 6)) + top# 490,500
        b = random.uniform(0.2, 0.4)
        pyautogui.moveTo(x, y, duration=b)
        b = random.uniform(0.01, 0.05)
        pyautogui.click(duration=b)
        return (x, y)
    else:
        print('No contours!')
        return False
def pick_random_fishing_spot(top_ss=0, left_ss=0, right_ss=800, bottom_ss=800, showCoords=False):
    left_ss, top_ss, right_ss, bottom_ss = 0, 0, 800, 800
    fish = find_fish(False, left_ss, top_ss, right_ss, bottom_ss)
    return fish

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
            print(bcolors.OK + f'time left: {(t_end - time.time())/60 :.2f} mins | status: {fishing_text} | fish: {fish_count} | clues: {clue_count} | {actions}| Drop at: {inv_cap}', end='')
        timer_log += 1
        time.sleep(1)
        if timer_log % 10 == 0:
            functions.screen_Image(0, 800, 0, 800)

def powerfisher(fish_type, Run_Duration_hours):
    global ibreak, coords, fishing_text, time_left, powerlist, actions, t_end, fish_count, clue_count, invent_count
    t_end = time.time() + (60 * 60 * Run_Duration_hours)

    print('Will break in: %.2f' % (ibreak / 60) + ' minutes |', "Fish Type Selected:", fish_type)
    t1 = Thread(target=timer_countdown)
    t1.start()

    while time.time() < t_end:
        global inv_cap
        randomizer(timer_break, ibreak)
        resizeImage()
        fishing_text = Image_to_Text('thresh', 'textshot.png')
        print(f'Emptying inv when at {inv_cap} items')
        approved_text = ['fishing', 'ishing', 'fishin']
        if fishing_text.strip().strip("'").strip(';').lower() not in approved_text:
            random_breaks(0.2, 3)
            pick_random_fishing_spot(fish_type)
            if random.randint(1,6) == 3:
                functions.offscreen_mouse()
            time.sleep(super_random_breaks(8, 11, 15, 18))
            resizeImage()
        # if skill_lvl_up() != 0:
        #     actions = 'level up'
        #     random_breaks(0.2, 3)
        #     pyautogui.press('space')
        #     random_breaks(0.1, 3)
        #     pyautogui.press('space')
        #     a = random.randrange(0, 2)
        #     # print(a)
        #     spaces(a)
        actions = 'none'
        invent_crop()
        resizeImage()
        # main_good = functions.invent_count(fish_type + '.png', .95)
        hammer = functions.invent_count('hammer.png', .75)
        fish_count = functions.invent_count(fish_type + '.png', .95)
        print(f'fish count is: {fish_count}')
        print(f'hammer count is: {hammer}')
        invent = fish_count
        if invent == 0:
            actions = 'opening inventory'
            screen_front(runelite)
            pyautogui.press('esc')
            time.sleep(random.randint(3, 6))
        if invent >= inv_cap:
            random_breaks(0.2, 0.7)
            drop_fish()
            random_breaks(0.2, 0.7)
            inv_cap = random.randint(14, 16)




coords = (0, 0)
actions = 'None'
fishing_text = 'Not Fishing'
time_left = 0

#-------------------------------

invent_count = 0

#use the other names to fly/cage fish
fish_type = functions.fish_type # 'trout_fish' # 'lobster_fish' 'salmon_fish', 'prawn_fish#
fish_count = 0
clue_count = 0
#-------------------------------

def rand_click(xrand, yrand):
    xrand = random.randrange(100, 450)
    yrand = random.randrange(250, 600)
    return xrand, yrand
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
    fish_count = functions.invent_count(fish_type + '.png', .95)
    x = xrand
    print(f'Right click x cord is: {x}')
    y = yrand
    print(f'Right click y cord is: {y}')
    pyautogui.click(x, y, button='right')
    ibreak = random.randrange(300, 2000)
    timer_break = timer()
    # --------- CHANGE TO RUN FOR AMOUNT OF HOURS ----------------
    Run_Duration_hours = random.uniform(4.5, 5.5)
    powerfisher(fish_type, Run_Duration_hours=Run_Duration_hours)
