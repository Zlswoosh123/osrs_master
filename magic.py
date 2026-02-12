import random
import time
import pyautogui
import win32gui
import core
import yaml
import login
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


def timer():
    startTime = time.time()
    return startTime


iflag = False

def move_mouse(x1, x2, y1, y2, click=False):
    b = random.uniform(0.15, 0.45)
    x_move = random.randrange(x1, x2) - 4
    y_move = random.randrange(y1, y2) - 4
    pyautogui.moveTo(x_move, y_move, duration=b)
    if click:
        pyautogui.click()

def high_alch_command():
    # 3rd item
    d = random.uniform(0.11, 0.18)
    time.sleep(d)
    pyautogui.click()
    print('alch command clicked')

def charge_staff():
    time.sleep(2.8)
    pyautogui.press('f4') # Open equipment menu
    time.sleep(random.uniform(.15, .5))
    move_mouse(655, 670, 568, 580) # Move to staff
    time.sleep(random.uniform(.15, .5))
    pyautogui.click() # Remove staff
    time.sleep(random.uniform(.15, .5))
    pyautogui.press('esc') # Open inventory
    time.sleep(random.uniform(1, 2))
    move_mouse(650, 660, 535, 550)  # Move to nature runes (1,2) x,y slot
    time.sleep(random.uniform(.15, .5))
    pyautogui.click()  # Click nats
    time.sleep(random.uniform(.15, .5))
    move_mouse(650, 660, 500, 510)  # Move to staff (1,1) x,y slot
    time.sleep(random.uniform(.15, .5))
    pyautogui.click()  # Click nats
    time.sleep(random.uniform(.15, .5))
    pyautogui.click()  # Click nats


def alch_check(): # todo add nat check
    functions.screen_Image(642, 676, 600, 632, 'alch_slot.png')
    alch = functions.image_count('empty_slot_alch.png', 'alch_slot.png')
    if alch > 0:
        print('Stop flag is True! No more alchs! Terminating script')
        return True
    if alch == 0:
        print(('Stop flag is False! We still have alchs! Keep going.'))
        return False

def nat_check():
    functions.screen_Image(642, 676, 525, 560, 'nat_slot.png')
    nat = functions.image_count('empty_slot.png', 'nat_slot.png')
    if nat > 0:
        print('Stop flag is True! No more nats! Terminating script')
        return True
    if nat == 0:
        print(('Stop flag is False! We still have nats! Keep going.'))
        return False



def high_alch_loop(vol=15, expensive=False, charge=False):
    t = vol
    charge_amt = t - (random.randint(900,1000))
    exp = expensive
    n = 5
    global stop_flag
    while t > 0 and stop_flag == False:
        wait_roll = random.randint(1,4000)
        wait_time_long = random.randint(45,260)
        wait_time_short = random.randint(15, 60)
        print(f'The anti-ban dice have been thrown! You rolled a {wait_roll}')
        if charge and t == vol:
            print(f'Bryophytas staff charging is enabled! Please ensure slot (1,1) is open and natures are directly below in (1,2)')
            charge_staff()
        if t < charge_amt and charge:
            charge_staff()
            n = 5
            charge_amt = t - (random.randint(900,1000))
        if wait_roll == 500:
            print(f'Weve initiated a long wait for anti-ban for {wait_time_long}s')
            time.sleep(wait_time_long)
            n = 5
        elif wait_roll % 800 == 0:
            print(f'Weve initiated a short wait for anti-ban for {wait_time_short}s')
            time.sleep(wait_time_short)
            n = 5
        else:
            pass
        if wait_roll % 50 ==  0 or t == vol:  # Check if alch inventory slot still has alchs
            time.sleep(1.8)
            pyautogui.press('f2')
            time.sleep(random.uniform(.1, .3))
            pyautogui.press('esc')
            # if alch_check() or nat_check():
            #     stop_flag = True
            pyautogui.press('f6')
            n = 5
        if wait_roll % 10 == 0 or n == 5:  # Fixes mouse location over high alch spot
            print(f'Were fixing mouse location and tab just in case')
            time.sleep(1.5)
            pyautogui.press('f2')
            time.sleep(random.uniform(.1,.3))
            pyautogui.press('f6')
            b = random.uniform(0.36, 0.52)
            x = random.randrange(796, 798) + 5
            print('x: ', x)
            y = random.randrange(584, 585) + 5
            print('y: ', y)
            d = random.uniform(0.11, 0.18)
            pyautogui.moveTo(x, y, duration=b)

        n = random.randint(6, 10)
        c = random.uniform(.05, .3)
        # pyautogui.press('f6')
        time.sleep(.1)
        # pyautogui.press('f6')
        high_alch_command()
        time.sleep(c)
        high_alch_command()  # alchs same spot as alch spell location
        c = random.uniform(1.8, 2.5)
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
    return True

if __name__ == "__main__":
    global stop_flag
    stop_flag = False
    round = 1
    max_round = 1
    while stop_flag == False and round <= max_round:
        # login.login('alt1login',house_tab=True)
        high_alch_loop(1568, expensive=False, charge=False)
        # login.logout()
        print(f'End of Round {round}')
        if round % 4 != 0:
            wait = random.uniform(1800, 2700)
            print(f'Short wait period before next round! Rolled {wait}s wait')
        else:
            wait = random.uniform(5400, 7200)
            print(f'Long wait period before next round! Rolled {wait}s wait')
        round += 1
        stop_flag = True
        time.sleep(wait)
        # time.sleep(10)
    # superheat_items(100, 1) #100 items iron
