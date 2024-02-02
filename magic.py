import random
import time
import pyautogui
import win32gui
import core
import yaml
# from functions import pick_item
# from functions import random_combat
# from functions import random_quests
# from functions import random_skills
# from functions import random_inventory
# from functions import random_breaks
#
# from functions import find_Object
# from functions import exit_bank
# from functions import Image_Rec_single
# from functions import deposit_secondItem

import functions

global hwnd
global iflag
global icoord
iflag = False
global newTime_break
newTime_break = False
global timer
global timer_break
global ibreak

def gfindWindow(data):  # find window name returns PID of the window
    global hwnd
    hwnd = win32gui.FindWindow(None, data)
    # hwnd = win32gui.GetForegroundWindow()860
    #print('findWindow:', hwnd)
    win32gui.SetActiveWindow(hwnd)
    # win32gui.ShowWindow(hwnd)
    win32gui.MoveWindow(hwnd, 0, 0, 865, 830, True)


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
    
def random_break(start, c):
    global newTime_break
    startTime = time.time()
    # 1200 = 20 minutes
    a = random.randrange(0, 4)
    if startTime - start > c:
        newTime_break = True


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


iflag = False


def high_alch_command():
    # 3rd item
    d = random.uniform(0.11, 0.18)
    time.sleep(d)
    pyautogui.click()
    print('alch command clicked')


# def high_alch():
#     # 3rd item
#     b = random.uniform(0.33, 0.46)
#     c = random.uniform(1, 1.5)
#     x = random.randrange(730, 750)
#     print('x: ', x)
#     y = random.randrange(490, 515) + 5
#     print('y: ', y)
#     d = random.uniform(0.11, 0.18)
#     pyautogui.moveTo(x, y, duration=b)
#     time.sleep(d)
#     pyautogui.click()
#
#     print('alching item')


def high_aclh_loop(vol, bool):
    t = vol
    exp = bool
    n = 5
    while t > 0:
        wait_roll = random.randint(1,1000)
        wait_time_long = random.randint(45,260)
        wait_time_short = random.randint(15, 60)
        print(f'The anti-ban dice have been thrown! You rolled a {wait_roll}')
        if wait_roll == 500:
            print(f'Weve initiated a long wait for anti-ban for {wait_time_long}s')
            time.sleep(wait_time_long)
            n = 5
        if wait_roll % 250 == 0:
            print(f'Weve initiated a short wait for anti-ban for {wait_time_short}s')
            time.sleep(wait_time_short)
            n = 5
        if n == 5:
            print(f'Were fixing mouse location and tab just in case')
            time.sleep(1.5)
            pyautogui.press('f2')
            time.sleep(random.uniform(.1,.3))
            pyautogui.press('f6')
            b = random.uniform(0.36, 0.52)
            x = random.randrange(640, 645) - 4
            print('x: ', x)
            y = random.randrange(605, 615) - 4
            print('y: ', y)
            d = random.uniform(0.11, 0.18)
            pyautogui.moveTo(x, y, duration=b)

        # n = random.randint(1, 10)
        c = random.uniform(.05, .3)
        # pyautogui.press('f6')
        time.sleep(.1)
        # pyautogui.press('f6')
        high_alch_command()
        time.sleep(c)
        high_alch_command()  # alchs same spot as alch spell location     #high_alch() alchs 3rd inventory spot
        c = random.uniform(1.4, 1.9)
        n = random.randint(1, 10)
        if exp:
            print('expensive')
            x = random.uniform(0.8, 1.2)
            time.sleep(x)
            x = random.uniform(0.8, 1.2)
            pyautogui.press('space')
            time.sleep(x)
            pyautogui.press('1')
            x = random.uniform(0.5, 0.6)
            time.sleep(x)
        time.sleep(c)
        # todo rename vars
        t -= 1
        print(f'{t} alchs remaining')


# def pick_iron_items():
#     pick_item(1510 - 1280, 123)
#     random_breaks(0.5, 1.5)
#
#
# def pick_bronze_items():
#     pick_item(1560 - 1280, 123)
#     random_breaks(0.5, 1.5)
#     pick_item(1607 - 1280, 123)
#     random_breaks(0.1, 0.5)
#
#
# def bank_spot_varrock():
#     find_Object(2)  # amber
#
#
# def cast_superheat():
#     pick_item(2029 - 1280, 573)
#
#
# def pick_ore(type):
#     Image_Rec_single(type, 'pick ores', 5, 5, 0.8, 'left', 20, 620, 480, False)
#
#
# def superheat_items(num, bar):
#     vol = [13, 27]
#     j = round(num / vol[bar])
#     pick_options = {0: pick_bronze_items,
#                     1: pick_iron_items}
#     orelist = ['copper.png', 'iron_ore.png']
#     while j > 0:
#         bank_spot_varrock()
#         random_breaks(0.3, 0.5)
#         deposit_secondItem()
#         random_breaks(0.3, 0.5)
#         pick_options[bar]()
#         exit_bank()
#         random_breaks(0.05, 0.2)
#         inv = 27
#         while inv != 0:
#             cast_superheat()
#             random_breaks(0.2, 0.4)
#             pick_ore(orelist[bar])
#             random_breaks(0.1, 0.2)
#             inv -= 1
#             print(inv)
#         j -= 1
#         random_breaks(0.4, 0.8)


if __name__ == "__main__":
    high_aclh_loop(750, False)
    # superheat_items(100, 1) #100 items iron
