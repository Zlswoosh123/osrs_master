
import datetime
import win32gui
from threading import Thread
import core
import yaml


import functions
from dataclasses import dataclass, field
from threading import Thread, Event, Lock
from functions import Image_count, invent_enabled
from functions import image_Rec_clicker
from functions import screen_Image
from functions import release_drop_item
from functions import drop_item
from functions import Image_to_Text
from functions import invent_crop
from functions import resizeImage
from functions import resize_quick
from PIL import ImageGrab

from functions import random_breaks
from functions import safe_open

import numpy as np
import cv2
import time
import random
import pyautogui

global hwnd
global iflag
global icoord
iflag = False
global timer
import slyautomation_title

inv_cap = random.uniform(14, 17)
print(f'Dropping ore at {inv_cap}')

class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR

@dataclass
class BotState:
    run_duration_hours: float = 4.5
    t_end: float = 0.0
    spot: tuple[int, int] | None = (0, 0)
    actions: str = "None"
    mined_text: str = "Not Mining"
    lock: Lock = field(default_factory=Lock)

    def time_left_str(self) -> str:
        remaining = max(0, self.t_end - time.time())
        return str(datetime.timedelta(seconds=round(remaining)))

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

def timer():
    startTime = time.time()
    return startTime

def Miner_Image_quick():
    left = 150
    top = 150
    right = 650
    bottom = 750

    im = ImageGrab.grab(bbox=(left, top, right, bottom))
    im.save('images/miner_img.png', 'png')

INVENT_CAPACITY = 28
INV_LEFT, INV_TOP, INV_RIGHT, INV_BOTTOM = 620, 460, 812, 735

def count_inventory_filled():
    """
    Counts non-empty inventory slots by detecting empty-slot tiles and subtracting from capacity.
    Requires an 'empty_slot.png' template captured from your inventory (no hover, no selection).
    """
    empties = Image_count(
        'empty_slot.png',
        threshold=0.88,
        left=INV_LEFT, top=INV_TOP, right=INV_RIGHT, bottom=INV_BOTTOM
    )
    filled = INVENT_CAPACITY - int(empties)
    # small guard against misreads when inventory isn’t open
    if filled < 0 or filled > INVENT_CAPACITY:
        return 0
    return filled

def Miner_Image():
    screen_Image(0, 865, 0, 830, 'images/miner_img.png')

def drop_ore():
    global actions
    actions = "drop ore."
    invent_crop()
    drop_item()
    image_Rec_clicker(r'copper_ore.png', 'dropping item', threshold=0.8, playarea=False)
    image_Rec_clicker(r'clay_ore.png', 'dropping item', threshold=0.8, playarea=False)
    image_Rec_clicker(r'coal_ore.png', 'dropping item', threshold=0.8, playarea=False)
    image_Rec_clicker(r'iron_ore.png', 'dropping item', threshold=0.8, playarea=False)
    image_Rec_clicker(r'tin_ore.png', 'dropping item', threshold=0.8, playarea=False)
    image_Rec_clicker(r'gem_icon.png', 'dropping item', threshold=0.8, playarea=False)
    image_Rec_clicker(r'gem_icon2.png', 'dropping item', threshold=0.8, playarea=False)
    release_drop_item()
    #print("dropping ore done")
    return "drop ore done"


def findarea_single(ore, cropx, cropy):
    Miner_Image_quick()
    image = cv2.imread(r"images/miner_img.png")
    safe_open(image, 'miner_img.png')

    # B, G, R ranges
    tin = ([103, 86, 65], [145, 133, 128])
    copper = ([35, 70, 120], [65, 110, 170])
    coal = ([20, 30, 30], [30, 50, 50])
    iron = ([15, 20, 40], [25, 40, 70])
    iron2 = ([17, 20, 42], [25, 38, 70])
    clay = ([50, 105, 145], [60, 125, 165])
    red = ([0, 0, 180], [80, 80, 255])
    green = ([0, 180, 0], [80, 255, 80])
    amber = ([0, 160, 160], [80, 255, 255])
    ore_list = [tin, copper, coal, iron, iron2, clay, red, green, amber]

    lower, upper = ore_list[ore]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)
    ret, thresh = cv2.threshold(mask, 40, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if not contours:
        # No target found
        return None

    # Largest contour
    c = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)

    # Guard against tiny boxes
    w = max(w, 6)
    h = max(h, 6)

    tx = random.randrange(x + 2, x + w - 1) + cropx
    ty = random.randrange(y + 2, y + h - 1) + cropy

    pyautogui.moveTo(tx, ty, duration=random.uniform(0.1, 0.3))
    pyautogui.click(duration=random.uniform(0.07, 0.11))
    return (tx, ty)

def count_gems():
    return Image_count('gem_icon.png', threshold=0.8, left=0, top=0, right=800, bottom=750)

def count_geo():
    return Image_count('geo_icon.png', threshold=0.8, left=0, top=0, right=800, bottom=750)

def count_gems2():
    return Image_count('gem_icon2.png', threshold=0.8, left=0, top=0, right=800, bottom=750)

def inv_count(name):
    return Image_count(name + '_ore.png', threshold=0.8, left=0, top=0, right=800, bottom=750)

def timer_printer(state: BotState, stop_event: Event):
    # prints once per second until stop_event is set or time expires
    while not stop_event.is_set() and time.time() < state.t_end:
        with state.lock:
            tl = state.time_left_str()
            spot = state.spot
            mined = state.mined_text
            act = state.actions
        print(
            bcolors.OK +
            f'\rtime left: {tl} | coords: {spot} | status: {mined} | ore: {ore} | {act}',
            end=''
        )
        time.sleep(1)

def count_items():
    global Run_Duration_hours
    t_end = time.time() + (60 * 60 * Run_Duration_hours)
    while time.time() < t_end:
        global ore, powerlist, mined_text
        time.sleep(0.1)
def print_progress(time_left, spot, mined_text, powerlist, ore, actions):
    print(bcolors.OK +
        f'\rtime left: {time_left} | coords: {spot} | status: {mined_text} | ore: {int(inv_count(powerlist[ore]))} | gems: {int(count_gems() + count_gems2())} | clues: {int(count_geo())} | {actions}',
        end='')

def powerminer_text(ore, num, Take_Human_Break=False, Run_Duration_hours=5):
    global inv_cap, powerlist
    runelite = functions.runelite
    powerlist = ['tin', 'copper', 'coal', 'iron', 'gold', 'clay', 'red', 'green', 'amber']

    # INIT SHARED STATE
    state = BotState(run_duration_hours=Run_Duration_hours)
    state.t_end = time.time() + (60 * 60 * state.run_duration_hours)

    # Start printer thread
    stop_event = Event()
    t1 = Thread(target=timer_printer, args=(state, stop_event), daemon=True)
    t1.start()

    print("Mine Ore Selected:", powerlist[ore])
    spot = (0, 0)  # local cursor target

    while time.time() < state.t_end:
        invent = int(inv_count(powerlist[ore]))
        if invent == 0:
            with state.lock:
                state.actions = 'opening inventory'
            try:
                window = win32gui.FindWindow(None, runelite)
                win32gui.ShowWindow(window, 5)
                win32gui.SetForegroundWindow(window)
                win32gui.SetActiveWindow(window)
                pyautogui.press('esc')
                time.sleep(random.uniform(2, 6))
            except Exception as err:
                print(f"An exception occurred: {err}")
                time.sleep(7)
        inventory = count_inventory_filled()

        with state.lock:
            state.actions = 'None'
        if inventory >= inv_cap:
            with state.lock:
                state.actions = 'dropping ore starting...'
            actions_result = drop_ore()
            with state.lock:
                state.actions = actions_result
            random_breaks(0.2, 0.7)
            inv_cap = random.uniform(14, 17)
            print(f'Dropping ore at {inv_cap}')

        resize_quick()
        resizeImage()
        mined_text_local = Image_to_Text('thresh', 'textshot.png').strip().lower()

        if mined_text_local not in ('mining', 'mininq'):
            mined_text_local = 'Not Mining'
            # Find a target; may return None
            new_spot = findarea_single(num, 150, 150)
            if new_spot is None:
                time.sleep(random.uniform(0.05, 0.2))
            if new_spot is not None:
                spot = new_spot
                if Take_Human_Break:
                    time.sleep(random.triangular(0.05, 6, 0.5))
        else:
            mined_text_local = 'Mining'

        with state.lock:
            state.mined_text = mined_text_local
            state.spot = spot

    # Stop the printer thread
    stop_event.set()
    t1.join(timeout=1.0)

spot = (0, 0)
actions = 'None'
mined_text = 'Not Mining'
time_left = 0

#-------------------------------

powerlist = ['tin', 'copper', 'coal', 'iron', 'gold', 'clay', 'red', 'green', 'amber']


#-------------------------------

if __name__ == "__main__":
    x = random.randrange(100, 250)
    y = random.randrange(400, 500)
    pyautogui.click(x, y, button='right')
    timer_break = timer()


    # ----- ORE -------
    tin = 0
    copper = 1
    coal = 2
    iron = 3
    gold = 4
    clay = 5

    # ----- OBJECT MARKER COLOR ------
    red = 6
    green = 7
    amber = 8

    # --------- CHANGE TO RUN FOR AMOUNT OF HOURS ----------------
    Run_Duration_hours = 4.5

                # | ore | marker color | take break | how long to run for in hours
    powerminer_text(tin, red, Take_Human_Break=True, Run_Duration_hours=Run_Duration_hours)

    #os.system('shutdown -s -f')
