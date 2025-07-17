import random
import time
import pyautogui
import win32gui
import core
import yaml

import functions
from functions import move_mouse

# ---------------------------
# LOAD WINDOW
# ---------------------------
def gfindWindow(data):
    global hwnd
    hwnd = win32gui.FindWindow(None, data)
    win32gui.SetActiveWindow(hwnd)
    win32gui.MoveWindow(hwnd, 0, 0, 865, 830, True)

with open("pybot-config.yaml", "r") as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)

try:
    gfindWindow(data[0]['Config']['client_title'])
except BaseException:
    print("Unable to find window:", data[0]['Config']['client_title'])
    core.printWindows()

try:
    x_win, y_win, w_win, h_win = core.getWindow(data[0]['Config']['client_title'])
except BaseException:
    print("Unable to get window dimensions.")
    core.printWindows()

# ---------------------------
# CONFIG (your real coords)
# ---------------------------
coords = {
    'bank_click': (138, 120),     # Coord 1 - click bank to withdraw p++
    'poison_slot': (740, 715),    # Coord 2 - inventory slot 27
    'ammo_slot': (777, 715),      # Coord 3 - inventory slot 28
    'bank_end': (420, 247),       # Coord 4 - click banker again
    'deposit_button': (490, 630), # NEW - Deposit Inventory button
}


loops_to_do = 10  # <-- how many full inventories to process

# ---------------------------
# HELPERS
# ---------------------------
def sleep_tick(base=0.6, variance=0.1, miss_chance=0.1):
    """Randomized delay ~OSRS tick; occasional late tick."""
    delay = base + random.uniform(-variance, variance)
    if random.random() < miss_chance:
        delay += random.uniform(0.2, 0.3)
    time.sleep(delay)

def move_and_click(x, y, rand=5, delay=0.15):
    """Use your move_mouse() then hover briefly before clicking."""
    move_mouse(x - rand, x + rand, y - rand, y + rand)
    time.sleep(delay)
    pyautogui.click()

# ---------------------------
# CORE ACTIONS
# ---------------------------
def reopen_bank():
    """Click bank, then click deposit all."""
    move_and_click(*coords['bank_end'])        # Open bank
    time.sleep(1.2)                             # Wait for bank UI to open
    move_and_click(*coords['deposit_button'])  # Click Deposit Inventory
    sleep_tick()

def withdraw_poison():
    """Click bank to withdraw p++; close bank."""
    move_and_click(*coords['bank_click'])
    sleep_tick()
    pyautogui.press('escape')   # close bank
    sleep_tick()

def apply_poison_once():
    """Click poison (slot 27) then ammo (slot 28)."""
    move_and_click(*coords['poison_slot'])
    sleep_tick(base=.1, variance=.08)
    move_and_click(*coords['ammo_slot'])
    # sleep_tick(base=.1, variance=.08)

def reopen_bank():
    """Click bank, then click deposit all."""
    move_and_click(*coords['bank_end'])        # Open bank
    time.sleep(1.2)                             # Wait for bank UI to open
    move_and_click(*coords['deposit_button'])  # Click Deposit Inventory
    sleep_tick()


# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    print(f"Starting weapon poison script for {loops_to_do} loop(s)...\n")
    print("⚠️  REMINDER: Make sure inventory slots 1 and 28 are locked (preserve poisoned ammo and unpoisoned ammo).")
    try:
        for loop_num in range(1, loops_to_do + 1):
            print(f"\n=== Loop {loop_num}/{loops_to_do} ===")
            withdraw_poison()

            for i in range(1, 27):  # 26 applications
                print(f"  Apply {i}/26")
                apply_poison_once()

            reopen_bank()

            # Small random human-ish pause between loops
            time.sleep(random.uniform(0.8, 1.6))

        print("\nAll loops complete. Script finished.")

    except KeyboardInterrupt:
        print("Script interrupted by user.")
    except pyautogui.FailSafeException:
        print("Failsafe triggered (mouse at top-left). Script stopped.")
