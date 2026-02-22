import time
import pyautogui
import win32gui
import core
import yaml


global hwnd
import functions2 as f2
import runtime_vars as v


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

Run_Duration_hours = v.run_duration_hours
t_end = time.time() + (60 * 60 * Run_Duration_hours)

if __name__ == "__main__":
    print('Startup Instructions: Ensure bank is opened and first item in tab is item to chisel')
    print('Ensure banker is tagged as pink and inventory is opened.')
    print('Ensure chisel is locked into 1st slot of invent.')
    t = (v.amount_to_do_chisel//27) + 1
    flag = v.chisel_flag # Determines if a second chisel is applied to gem to make tips
    while t > 0 and time.time() < t_end:
        f2.move_mouse(125, 140, 120,130, click=True) # move to first item in bank
        f2.random_wait(.05, .2)

        pyautogui.press('escape')
        f2.random_wait(.65, .85)

        f2.move_mouse(*f2.inventory_spots[0], click=True)  # move to first obj in inv (next box)
        f2.random_wait(.05, .2)

        f2.move_mouse(*f2.inventory_spots[1], click=True)  # move to 2nd obj in inv (nests)
        f2.random_wait(1, 1.2)
        pyautogui.press('space')
        f2.random_wait(33, 41)

        if flag == True:
            f2.move_mouse(*f2.inventory_spots[0], click=True)  # move to first obj in inv (next box)
            f2.random_wait(.05, .2)

            f2.move_mouse(*f2.inventory_spots[1], click=True)  # move to 2nd obj in inv (nests)
            f2.random_wait(1, 1.2)
            pyautogui.press('space')
            f2.random_wait(80, 88)

        if v.breaks:
            f2.random_afk_roll()

        f2.click_color_bgr_in_region(target_bgr=f2.PINK_BGR, region=(0, 180, 600, 635),click=True) # click banker (pink)
        f2.random_wait(.6, 4)

        f2.move_mouse(*f2.special_spots['empty'], click=True)  # empty all
        f2.random_wait(.7, 3)
        t -= 1
        print(f'{t} actions remaining')

        if v.breaks:
            f2.random_afk_roll()
