import win32gui
import core
import yaml
from functions import (Image_count, invent_enabled,
                       move_mouse, click_object, screen_Image, Image_to_Text, resizeImage)
from PIL import ImageGrab, Image
import functions2 as f2
import os, re
import numpy as np
import cv2
import time
import random
import pyautogui
import pytesseract

from functions2 import icon_check, bank_spots, inventory_spots, inv_count, special_spots

global hwnd
global iflag
global icoord
iflag = False

def gfindWindow(data):  # find window name returns PID of the window
    global hwnd
    hwnd = win32gui.FindWindow(None, data)
    # hwnd = win32gui.GetForegroundWindow()860
    #print('findWindow:', hwnd)
    win32gui.SetActiveWindow(hwnd)
    # win32gui.ShowWindow(hwnd)
    win32gui.MoveWindow(hwnd, 0, 0, 865, 830, True) #(hwnd, 0, 0, 865, 830, True)


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

def ensure_client_foreground():
    """Bring the client window to the front (best-effort; safe if it fails)."""
    try:
        window = win32gui.FindWindow(None, data[0]['Config']['client_title'])
        win32gui.ShowWindow(window, 5)
        win32gui.SetForegroundWindow(window)
        win32gui.SetActiveWindow(window)
    except Exception:
        pass

INVENT_CAPACITY = 28
INV_LEFT, INV_TOP, INV_RIGHT, INV_BOTTOM = 620, 460, 812, 735

def click_client(x, y, jitter=0, move_dur=(0.12, 0.25)):
    x0, y0 = get_client_origin()
    tx = x0 + x + random.randint(-jitter, jitter)
    ty = y0 + y + random.randint(-jitter, jitter)
    pyautogui.moveTo(tx, ty, duration=random.uniform(*move_dur))
    pyautogui.click()

def get_client_origin():
    """
    Return (x0, y0) top-left of client window, always without raising NameError.
    Caches into x_win/y_win/w_win/h_win globals when we discover them.
    """
    global x_win, y_win, w_win, h_win
    x0 = globals().get('x_win', 0)
    y0 = globals().get('y_win', 0)
    if x0 == 0 and y0 == 0:
        # Try core.getWindow first
        try:
            x_win, y_win, w_win, h_win = core.getWindow(data[0]['Config']['client_title'])
            x0, y0 = x_win, y_win
        except Exception:
            # Win32 fallback
            try:
                hwnd_local = win32gui.FindWindow(None, data[0]['Config']['client_title'])
                l, t, r, b = win32gui.GetWindowRect(hwnd_local)
                x_win, y_win, w_win, h_win = l, t, r - l, b - t
                x0, y0 = x_win, y_win
            except Exception:
                # Leave (0,0); caller may warn if window isn't pinned there
                x0, y0 = 0, 0
    return x0, y0


def grab_client_region(region=None):
    x0, y0 = get_client_origin()
    ww = globals().get('w_win', 0)
    hh = globals().get('h_win', 0)

    if region is None:
        left, top = x0, y0
        right  = x0 + (ww or 865)   # fallback to your MoveWindow width if you pin it
        bottom = y0 + (hh or 830)
    else:
        l, t, r, b = region
        left, top, right, bottom = x0 + l, y0 + t, x0 + r, y0 + b

    im = ImageGrab.grab(bbox=(left, top, right, bottom))
    bgr = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
    return bgr, (left, top)



def random_wait(a=.1, b=.3):
    c = random.uniform(a, b)
    time.sleep(c)

def temp_change():
    print('temp_change detected! Starting now')
    f2.click_color_bgr_in_region(target_bgr=f2.PINK_BGR, region=f2.SEARCH_REGION)
    pyautogui.moveRel(0, 50)
    end = False
    count = 0
    wait = random.uniform(7,10)
    reclick_timer = time.time() + wait
    while count <= 1 and end == False:
        # print('Pink region found, should be actively for temp')
        color_check = f2.click_color_bgr_in_region(target_bgr=f2.PINK_BGR, region=f2.SEARCH_REGION, click=False)[0]
        if color_check:
            count = 0
            if time.time() > reclick_timer:
                f2.click_color_bgr_in_region(target_bgr=f2.PINK_BGR, region=f2.SEARCH_REGION)
                pyautogui.moveRel(0, 50)
                wait = random.uniform(5, 7)
                reclick_timer = time.time() + wait
        else:
            print('Missing color, count is: ', count)
            count += 1
            time.sleep(.05)
    print('Ending temp_change now')

def make_sword():
    print('make_sword check starting!')
    f2.click_color_bgr_in_region(target_bgr=f2.GREEN_BGR, region=f2.SEARCH_REGION)
    pyautogui.moveRel(0,50)
    time.sleep(.01)
    timer = time.time() + 25
    end = False
    count = 0
    while count < 1 and end == False:
        color_check = f2.click_color_bgr_in_region(target_bgr=f2.GREEN_BGR, region=f2.SEARCH_REGION, debug=False, click = False)[0]
        # color_check_sp = f2.click_color_bgr_in_region(target_bgr=f2.PURPLE_BGR, region=f2.SEARCH_REGION, debug=False, click = False)[0]
        #
        # if color_check_sp:
        #     f2.click_color_bgr_in_region(target_bgr=f2.PURPLE_BGR, region=f2.SEARCH_REGION, debug=False, click=True)

        if color_check:
            # print('Green region found, should be actively making sword')
            count = 0
        else:
            print('Missing color, count is: ', count)
            count += 1
            # time.sleep(.05)
        if time.time() > timer:
            print('Timer has expired for make_sword! Exiting function for safety')
            end = True
    print('make_sword check ending!')

def turn_in():
    print('turn_in start')
    # Turn in sword and get new commission

    while f2.icon_check(name = 'GF_Menu.png',image = 'menu_title.png',
                        left=170, top=182, right=450, bottom=215) == 0 and f2.click_color_bgr_in_region(target_bgr=f2.PINK_BGR,
                                 region=f2.SEARCH_REGION, debug=False, click=False)[0] == False:
        f2.click_color_bgr_in_region(target_bgr=f2.BLUE_BGR, region=f2.SEARCH_REGION)
        time.sleep(6)
        pyautogui.press('space')
        time.sleep(1)
        pyautogui.press('space')
        time.sleep(1)
        pyautogui.press('1')
        time.sleep(1)
        f2.click_color_bgr_in_region(target_bgr=f2.BLUE_BGR, region=f2.SEARCH_REGION)
        time.sleep(2)
    print('turn_in end')

def select_mould():
    print('select_mould start')
    min = .6
    max = 1.5
    while f2.icon_check(name='GF_Menu.png', image='menu_title.png',
                        left=170, top=182, right=450, bottom=215) == 1 and f2.click_color_bgr_in_region(target_bgr=f2.PINK_BGR,
                                 region=f2.SEARCH_REGION, debug=False, click=False)[0] == False:
        move_mouse(105,150,315, 324, True) # Selects Forte Menu
        time.sleep(random.uniform(min,max))
        move_mouse(268, 384, 325, 333, True)  # Selects Forte
        time.sleep(random.uniform(min,max))

        move_mouse(105, 150, 355, 365, True)  # Selects Blades Menu
        time.sleep(random.uniform(min,max))
        move_mouse(268, 384, 325, 333, True)  # Selects Blades
        time.sleep(random.uniform(min,max))

        move_mouse(105, 150, 397, 408, True)  # Selects Tips Menu
        time.sleep(random.uniform(min,max))
        move_mouse(268, 384, 325, 333, True)  # Selects Tips
        time.sleep(random.uniform(min,max))

        move_mouse(438, 480, 270, 282, True)  # Selects Tips Menu
        time.sleep(random.uniform(min, max))
    print('select_mould end')

def withdraw_metals():
    print('withdraw_metals start')
    while icon_check() == 0: # Clicks bank chest
        f2.click_color_bgr_in_region(target_bgr=f2.YELLOW_BGR, region=f2.SEARCH_REGION)
        time.sleep(random.randint(4,6))
    # Performs grabbing of bars in bank
    move_mouse(*bank_spots[0], click=True)
    time.sleep(random.uniform(.1,.7))
    move_mouse(*bank_spots[1], click=True)
    time.sleep(random.uniform(.6, 1))
    pyautogui.press('escape')
    time.sleep(random.uniform(.6, 1))

    count = inv_count('bar.png')
    if count < 28:
        withdraw_metals()
    print('withdraw_metals end')

def add_metals(metal1='mithril', metal2='adamant'):
    print('add_metals start')
    failsafe = 0
    metals = {
        'bronze': '1',
        'iron': '2',
        'steel:': '3',
        'mithril': '4',
        'adamant': '5',
        'rune': '6'
              }
    while inv_count('bar.png') > 2 and f2.click_color_bgr_in_region(target_bgr=f2.BLUE_BGR,
                                 region=f2.SEARCH_REGION, debug=False, click=False)[0] == True:
        f2.click_color_bgr_in_region(target_bgr=f2.BLUE_BGR, region=f2.SEARCH_REGION)
        time.sleep(random.uniform(3, 4.5))
        pyautogui.press(metals[metal1])
        time.sleep(random.uniform(1.6, 3))
        f2.click_color_bgr_in_region(target_bgr=f2.BLUE_BGR, region=f2.SEARCH_REGION)
        time.sleep(random.uniform(.6, 1.5))
        pyautogui.press(metals[metal2])
        time.sleep(random.uniform(4, 5))

        if failsafe > 5:
            print('add_metals failed via failsafe')
            while icon_check() == 0:  # Clicks bank chest
                f2.click_color_bgr_in_region(target_bgr=f2.YELLOW_BGR, region=f2.SEARCH_REGION)
                time.sleep(random.randint(4, 6))
                move_mouse(*special_spots['empty'], click=True)
                time.sleep(random.uniform(1.3,3))
                pyautogui.press('escape')
                time.sleep(2)
        failsafe += 1
    print('add_metals end')


def pour_mould():
    print('pour_mould start')
    failsafe = 0
    f2.click_color_bgr_in_region(target_bgr=f2.GREEN_BGR, region=f2.SEARCH_REGION)
    time.sleep(random.randint(6,8))
    while f2.click_color_bgr_in_region(target_bgr=f2.PINK_BGR,
                                 region=f2.SEARCH_REGION, debug=False, click=False)[0] == False:
        f2.click_color_bgr_in_region(target_bgr=f2.BLUE_BGR, region=f2.SEARCH_REGION)
        time.sleep(random.randint(4, 7))
        failsafe += 1
        if failsafe > 5:
            print('pour_mould failsafe triggered!')
            time.sleep(999999999)
    print('pour_mould end')
time_left = 0
#-------------------------------

if __name__ == "__main__":
    Run_Duration_hours = 1.5
    t_end = time.time() + (60 * 60 * Run_Duration_hours)

    metal1 = 'mithril'
    metal2 = ('adamant'
              '')
    while time.time() < t_end:
        # Ensure right sword temp (Pink)
        if f2.click_color_bgr_in_region(target_bgr=f2.PINK_BGR, region=f2.SEARCH_REGION, click=False)[0]:
            temp_change()
        time.sleep(.01)
        # else:1
        #     print('No pink detected for temp change')

        # Go to equipment (Green)
        if f2.click_color_bgr_in_region(target_bgr=f2.GREEN_BGR, region=f2.SEARCH_REGION, click=False)[0]:
            make_sword()

        # Turn-in and Restock
        if ((f2.click_color_bgr_in_region(target_bgr=f2.PURPLE_BGR, region=f2.SEARCH_REGION, click=False)[0]
                or f2.click_color_bgr_in_region(target_bgr=f2.BLUE_BGR, region=f2.SEARCH_REGION, click=False)[0])and
            f2.click_color_bgr_in_region(target_bgr=f2.PINK_BGR, region=f2.SEARCH_REGION, click=False)[0] == False):
            turn_in()
            select_mould()
            withdraw_metals()
            add_metals(metal1, metal2)
            pour_mould()