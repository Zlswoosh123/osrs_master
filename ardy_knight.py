import random
import time
import pyautogui
import win32gui
import core
import yaml


import functions
from functions import inventory_spots, move_mouse, click_object

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

iflag = False

def random_wait(a=.1, b=.3):
    c = random.uniform(a, b)
    time.sleep(c)



if __name__ == "__main__": # Fixed version for vm
    # --- SETTINGS ---
    x1, y1 = 423, 530  # Position of the knight
    x2, y2 = 654, 501  # Position of coin pouch
    clicks_per_cycle = 100  # Number of pickpockets per cycle
    max_repeats = 2  # Maximum number of full pickpocket+pouch cycles

    # --- LOOP ---
    try:
        print(f"Starting... Will run for {max_repeats} cycles. Move mouse to top-left to stop.")

        for cycle in range(max_repeats):
            print(f"Cycle {cycle + 1} of {max_repeats}")

            # Click the knight multiple times
            for i in range(clicks_per_cycle):
                pyautogui.click(x1, y1)
                delay = random.uniform(0.5, 1.25)
                time.sleep(delay)
                print('Clicked ', i, 'times out of ', clicks_per_cycle, ' on cycle ', cycle + 1, ' of ', max_repeats)

            # Click the coin pouch spot once
            time.sleep(3)
            pyautogui.click(x2, y2)
            time.sleep(random.uniform(0.6, 1.2))  # Optional delay before next cycle

        print("Done. All cycles completed.")

    except KeyboardInterrupt:
        print("Stopped by user.")
    except pyautogui.FailSafeException:
        print("Failsafe triggered — mouse moved to corner.")
