import yaml
import win32gui
import core
import pyautogui
import time
import random
import tkinter as tk
from tkinter import messagebox
from ahk import AHK

def gfindWindow(data):  # Find window name and set as active
    global hwnd
    hwnd = win32gui.FindWindow(None, data)
    if hwnd == 0:
        raise Exception(f"Unable to find window: {data}")
    win32gui.SetActiveWindow(hwnd)
    win32gui.MoveWindow(hwnd, 0, 0, 865, 830, True)

with open("pybot-config.yaml", "r") as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)

try:
    gfindWindow(data[0]['Config']['client_title'])
except Exception as e:
    print(e)
    core.printWindows()
    exit()

try:
    x_win, y_win, w_win, h_win = core.getWindow(data[0]['Config']['client_title'])
except Exception as e:
    print(e)
    core.printWindows()
    exit()

# Initialize AHK
ahk = AHK(executable_path="C:\\Program Files\\AutoHotkey\\v1.1.37.02\\AutoHotkeyU64.exe")

def main_script():
    # # Clear input
    # ahk.run_script("""
    # SendMode Input
    # Send, {Ctrl Down}{Backspace Down}{Backspace Up}{Ctrl Up}
    # """)
    #
    # # Type `::hop 534` at the start of the script
    # ahk.run_script("""
    # SendMode Input
    # Send, ::hop 534{Enter}
    # """)
    # time.sleep(10)

    # Set a random loop limit between 27 and 30
    loop_limit = 28 # random.randint(27, 29)
    print(f"Looping {loop_limit} times.")

    for i in range(loop_limit):
        print(f"Iteration {i + 1}/{loop_limit}")

        # Step 1: Click a tile to pick up the item
        tile_x, tile_y = random.randint(410,414), random.randint(418,422)  # Example coordinates
        pyautogui.click(tile_x, tile_y)
        time.sleep(random.randint(60,65))  # Pause to ensure the click is registered

        # # Step 2: Use CTRL+SHIFT+LEFT to hop worlds
        # ahk.run_script("""
        # SendMode Input
        # Send, {Ctrl Down}{Shift Down}{Left}{Shift Up}{Ctrl Up}
        # """)
        # time.sleep(random.randint(20, 25))  # Allow time for the world to load

    print("Script has completed the loop limit.")
    repeat_prompt()

def repeat_prompt():
    # Create a new Tkinter instance for each prompt
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window
    response = messagebox.askyesno("Repeat Script", "Do you want to repeat the script?")
    if response:
        root.destroy()  # Destroy the current Tkinter instance
        main_script()  # Restart the script
    else:
        root.destroy()  # Destroy the current Tkinter instance
        print("Exiting script.")

if __name__ == "__main__":
    main_script()