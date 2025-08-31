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
    win32gui.SetActiveWindow(hwnd)
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

# ---------------------------
# CONFIGURATION (REAL COORDINATES)
# ---------------------------
coords = {
    'seaweed_slot': (138, 120),         # Giant seaweed in bank
    'sand_slot': (200, 100),            # Bucket of sand in bank
    'inventory_close': (300, 100),      # Close bank button
    'spell_button': (640, 593),         # Superglass Make spell
    'glass_pickup': (421, 523),         # Ground glass pile (not used yet)
    'banker': (420, 247),               # Clickable banker location
    'deposit_all': (490, 630),          # Deposit All button in bank (replace with actual)
}

casts_to_do = 50  # Total casts you want to do

# ---------------------------
# FUNCTIONS
# ---------------------------

def click(x, y, rand=5):
    """Click with small random offset for humanization."""
    offset_x = random.randint(-rand, rand)
    offset_y = random.randint(-rand, rand)
    pyautogui.click(x + offset_x, y + offset_y)


def sleep_tick(base=0.6, variance=0.1, miss_chance=0.1):
    """Sleep with randomness to simulate OSRS ticks."""
    delay = base + random.uniform(-variance, variance)
    if random.random() < miss_chance:
        delay += random.uniform(0.2, 0.3)
    time.sleep(delay)


def withdraw_items():
    """Withdraw 3 giant seaweed and 18 buckets of sand from bank."""
    for _ in range(1):
        move_mouse(129, 133, 123, 127, click=True)  # seaweed slot
        sleep_tick()

    for _ in range(6):
        move_mouse(180, 185, 123, 127,click=True)  # sand slot
        sleep_tick(.2,miss_chance=0)

    pyautogui.press('escape')
    sleep_tick(0.8)  # Wait for bank to close


def cast_superglass_make():
    """Switch to spellbook, cast Superglass Make, then return to inventory."""
    pyautogui.press('f6')  # Switch to spellbook tab
    sleep_tick(0.2, 0.05)

    click(*coords['spell_button'])  # Cast the spell
    time.sleep(random.uniform(1.3, 1.7))  # Wait for animation to complete

    pyautogui.press('escape')  # Return to inventory
    sleep_tick(1.3, 0.05)


def deposit_items():
    """Click banker, deposit all, pickup glass, then deposit again."""

    # --- First interaction: Open bank ---
    move_mouse(coords['banker'][0] - 5, coords['banker'][0] + 5,
               coords['banker'][1] - 5, coords['banker'][1] + 5)
    time.sleep(0.15)
    pyautogui.click()
    time.sleep(1.2)  # Ensure bank UI opens

    move_mouse(coords['deposit_all'][0] - 5, coords['deposit_all'][0] + 5,
               coords['deposit_all'][1] - 5, coords['deposit_all'][1] + 5)
    time.sleep(0.15)
    pyautogui.click()
    sleep_tick()

    # --- Pickup glass ---
    # pickup_glass()

    # --- Second interaction: Reopen bank and deposit again ---
    # move_mouse(coords['banker'][0] - 5, coords['banker'][0] + 5,
    #            coords['banker'][1] - 5, coords['banker'][1] + 5)
    # time.sleep(0.15)
    # pyautogui.click()
    # time.sleep(1.2)

    # move_mouse(coords['deposit_all'][0] - 5, coords['deposit_all'][0] + 5,
    #            coords['deposit_all'][1] - 5, coords['deposit_all'][1] + 5)
    # time.sleep(0.15)
    # pyautogui.click()
    # sleep_tick()



def pickup_glass():
    """Pick up molten glass from the ground."""
    pyautogui.press('escape')  # Close bank
    sleep_tick(0.2, 0.05)

    clicks = random.randint(4, 7)
    for _ in range(clicks):
        move_mouse(coords['glass_pickup'][0] - 5, coords['glass_pickup'][0] + 5,
                   coords['glass_pickup'][1] - 5, coords['glass_pickup'][1] + 5)
        time.sleep(0.15)
        pyautogui.click()
        sleep_tick(.5, .1, 0)



# ---------------------------
# MAIN LOOP
# ---------------------------
try:
    print(">>> Starting Superglass Make script...")
    print("Instructions:")
    print(" - Start with bank open at Ferox Enclave")
    print(" - Ensure 'Select-X' is set to 3 for seaweed")
    print(" - Ensure you are on the Lunar spellbook and have the spell visible or hotkeyed")
    print(" - Smoke Battlestaff or equivalent is equipped\n")

    print(f"Running for {casts_to_do} casts.\n")

    for cast_num in range(1, casts_to_do + 1):
        withdraw_items()
        cast_superglass_make()
        deposit_items()  # Reopen bank and deposit all after each cast

        remaining = casts_to_do - cast_num
        progress = round((cast_num / casts_to_do) * 100, 1)
        print(f"[{cast_num}/{casts_to_do}] Cast complete — {remaining} to go ({progress}% done)")

        time.sleep(random.uniform(0.6, 1.2))

    print("\nAll casts completed. Script finished.")

except KeyboardInterrupt:
    print("Script interrupted by user.")
except pyautogui.FailSafeException:
    print("Failsafe triggered (mouse moved to top-left corner). Script stopped.")
