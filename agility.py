
import win32gui
import numpy as np
import cv2
import pyautogui
import random
import time
import functions
import core
import yaml
from functions import screen_Image
from functions import safe_open
from functions import double_random

# Variables
global hwnd
timer_log = 0
runelite = functions.runelite
window = functions.window


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


fish_lower = [110, 100, 0] # 00FFFF
fish_upper = [195, 180, 60]
blue_lower = [120, 20, 20] # 1300FF #stored: blue_lower = [90, 10, 20] # 1300FF
blue_upper = [150, 210, 90] # blue_upper = [130, 200, 80]
# extra blue values? purple_lower = [140, 20, 30] # FF00FF # store: purple_lower = [140, 20, 20] # FF00FF
# purple_upper = [180, 150, 60]
yellow_lower = [0, 100, 150] # #FFFF00
yellow_upper = [50, 255, 255]
red_lower = [0, 150, 125] # FF0000
red_upper = [0, 255, 255]
yellow, red, blue = [yellow_lower, yellow_upper], [red_lower, red_upper],[blue_lower, blue_upper]
black_lower = [0, 0, 0] # 000000
black_upper = [255, 255, 255]
purple_lower = [120, 0, 100]
purple_upper = [220, 100, 200] # done?
green_lower = [50, 100, 0] 	# 00FF00
green_upper = [65, 180, 60]
def find_fish(showCoords=False, left=0, top=0, right=800, bottom=800, boundaries=[(fish_lower, fish_upper)]):
    global window
    functions.screen_Image(left, top, right, bottom) # take screenshot
    screen_Image(0, 0, 800, 800)
    image = cv2.imread('images/screenshot.png')
    safe_open(image, 'screenshot.png')
    functions.screen_block(image) # block out inventory, chat, and map
    cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

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
            # Apply morphological operations to remove small white dots
            kernel = np.ones((1, 1), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            # Apply mask threshold and find contours
            ret, thresh = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

            # Create a blank image with the same size as the original image
            filled_image = np.zeros_like(image)

            # Draw and fill contours on the blank image
            cv2.drawContours(filled_image, contours, -1, (255, 255, 255), thickness=cv2.FILLED)
            cv2.imshow('filled', filled_image)
            # Visualize the mask
            # cv2.imshow('Mask', mask)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    if len(contours) != 0:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        print(f'Coords: x is:{x}, y is:{y}, w is:{w}, h is:{h}')
        whalf = max(round(w / 2), 1)
        hhalf = max(round(h / 2), 1)
        x = random.randrange(x + 5, x + max(whalf - 5, 6)) + left  # 950,960
        y = random.randrange(y + 5, y + max(hhalf - 5, 6)) + top - 5 # 490,500
        b = random.uniform(0.2, 0.4)
        pyautogui.moveTo(x, y, duration=b)
        b = random.uniform(0.01, 0.05)
        pyautogui.click(duration=b)
        return (x, y)
    else:
        print('No contours found!')
        return False

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
            print(bcolors.OK + f'\r[%-10s] %d%%' % ('='*round((i/final)*10), round((i/final)*100)), f'time left: {(t_end - time.time())/60 :.2f} mins', end='')
        timer_log += 1


def agility_run( Run_Duration_hours):
    t_end = time.time() + (60 * 60 * Run_Duration_hours)
    while time.time() < t_end:
        screen_Image(0, 0, 800, 800)
        find_fish(boundaries=[(fish_lower, fish_upper)])
        # find_fish(boundaries=[(red_lower, red_upper)])
        time.sleep(double_random(3,5))
        screen_Image(0, 0, 800, 800)
        find_fish(boundaries=[(yellow_lower, yellow_upper)])
        time.sleep(double_random(3,5))
        screen_Image(0, 0, 800, 800)
        find_fish(boundaries=[(purple_lower, purple_upper)])
        time.sleep(double_random(3,5))
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
    screen_Image(0, 0, 555, 660)
    x = xrand
    print(f'Right click x cord is: {x}')
    y = yrand
    print(f'Right click y cord is: {y}')
    pyautogui.click(x, y, button='right')
    # --------- CHANGE TO RUN FOR AMOUNT OF HOURS ----------------
    Run_Duration_hours = random.uniform(4.5, 5.5)
    agility_run(Run_Duration_hours=Run_Duration_hours)
