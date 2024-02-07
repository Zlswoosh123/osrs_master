import time
import random
import pyautogui

import functions as f

def login(account:str,house_tab=False):
    f.screen_Image(210,620, 200, 420,'loginarea.png')
    f.screen_Image(220, 620, 300, 450, 'redbox.png')
    count = f.image_count('loginarea.png', 'existing_user.png', .7)
    box_count = f.image_count('redbox.png', 'clickplay.png', .7)
    fail_safe = 0
    if count == 1:
        f.move_mouse(490, 491, 335, 336, True)  # Click existing user
        time.sleep(.5)
        pyautogui.typewrite(account)  # Uses ahk to load creds
        time.sleep(.2)
        pyautogui.press('tab')
        time.sleep(.5)
        f.move_mouse(300, 305, 360, 365, True)  # Clicks login
        f.move_mouse(25, 26, 25, 26, False)  # Moves mouse away
        while box_count != 1 and fail_safe < 25:
            print(f'No red box found, waiting! Attempt {fail_safe}')
            time.sleep(2)
            f.screen_Image(220, 620, 300, 450, 'redbox.png')
            box_count = f.image_count('redbox.png', 'clickplay.png', .9)
            fail_safe += 1
        if fail_safe >= 25:
            print('Fail safe triggered, login failed!')
            return False
        f.move_mouse(370, 450, 360, 380, True)  # Presses red continue box to login
        time.sleep(6)
        pyautogui.press('f4')  # Open equipment menu
        time.sleep(1)
        pyautogui.press('esc')  # Open inventory
        time.sleep(1)
        if house_tab:
            # f.move_mouse(770, 780, 700, 710, True) old coords
            print('clicking teletab')
            f.move_mouse(775, 785, 715, 720, True)
            time.sleep(5)# Clicks home tele in bottom right of inv
        return True
    elif count >= 2:
        print('Found more than 1 existing user? Skipping')
    else:
        print('Found no login button, login failed')
        return False

    print(count)

if __name__ == "__main__":
    login('alt2login')