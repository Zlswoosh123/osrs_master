import time
import pyautogui
import win32gui
import core
import yaml
from functions import inventory_spots
import functions2 as f2
import runtime_vars as v

global hwnd



def gfindWindow(data):  # find window name returns PID of the window
    global hwnd
    hwnd = win32gui.FindWindow(None, data)
    # hwnd = win32gui.GetForegroundWindow()860
    # print('findWindow:', hwnd)
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



type = v.potion_mixing_type # 1 for creating unf, 2 for creating potions
Run_Duration_hours = v.run_duration_hours
t_end = time.time() + (60 * 60 * Run_Duration_hours)

if __name__ == "__main__":
    print('Start in Bank screen. Order: Pie Shell, Beef, Chompy, Rabbit')
    print('Ensure banker is tagged as pink and inventory is opened. Withdraw X=7')
    t = (v.amount_to_do_herb //7) + 1
    while t > 0 and time.time() < t_end:
        f2.move_mouse(*f2.bank_spots[0], click=True) # move to first item in bank
        f2.random_wait(.2, .3)

        f2.move_mouse(*f2.bank_spots[1], click=True) # move to 2nd item in bank
        f2.random_wait(.05, .2)

        f2.move_mouse(*f2.bank_spots[2], click=True) # move to 3rd item in bank
        f2.random_wait(.05, .2)

        f2.move_mouse(*f2.bank_spots[3], click=True) # move to 4th item in bank
        f2.random_wait(.05, .2)

        pyautogui.press('escape')
        f2.random_wait(.05, .1)

        # Start combine logic here
        l = [10, 14, 22]
        for i in l:
            f2.move_mouse(*inventory_spots[6], click=True)  # Click shell
            f2.random_wait(.05, .2)

            f2.move_mouse(*inventory_spots[i], click=True)  # move to 2nd obj in inv (nests)
            f2.random_wait(1, 1.2)
            pyautogui.press('space')
            f2.random_wait(7*1.2, 9*1.2)  # Wait for processing


        if v.breaks:
            f2.random_afk_roll(100)

        f2.click_color_bgr_in_region(target_bgr=f2.PINK_BGR, region=(0, 180, 600, 635),click=True) # click banker (pink)
        f2.random_wait(.6, 4)

        f2.move_mouse(*f2.special_spots['empty'], click=True)  # empty all
        f2.random_wait(.7, 3)

        t -= 1
        print(f'{t} actions remaining')
        if v.breaks:
            f2.random_afk_roll(100)
