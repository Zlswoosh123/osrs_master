import time
import random
import pyautogui
import functions as f

def ok_check():
    f.screen_Image(255, 550, 280, 360, 'disconnect_check.png')
    count = f.image_count('ok_button.png', 'disconnect_check.png')
    if count > 0:
        return True
    if count == 0:
        return False

def login(account:str,house_tab=False):
    f.screen_Image(210,620, 200, 420,'loginarea.png')
    f.screen_Image(220, 620, 300, 450, 'redbox.png')
    disconnect = f.image_count('ok_button.png', 'loginarea.png', .7)
    print(disconnect)
    fail_safe = 0
    ok = ok_check()
    if ok:
        print('We see an ok button, clearing')
        f.move_mouse(421, 425, 330, 331, True)  # failsafe for disconnect, clicks OK button
    else:
        print('No OK button found')
    time.sleep(1)
    count = f.image_count('existing_user.PNG', 'loginarea.png', .9)
    print(f'count is {count}')
    box_count = f.image_count('redbox.png', 'clickplay.png', .6)
    if count >= 1:
        f.move_mouse(490, 491, 335, 336, True)  # Click existing user
        time.sleep(.5)
        pyautogui.typewrite(account)  # Uses ahk to load creds
        time.sleep(.2)
        pyautogui.press('tab')
        time.sleep(.5)
        f.move_mouse(300, 305, 360, 365, True)  # Clicks login
        f.move_mouse(45, 46, 45, 46, False)  # Moves mouse away
        print(f'box count is {box_count}')
        while box_count <= 1 and fail_safe < 25:
            print(f'No red box found, waiting! Attempt {fail_safe}')
            time.sleep(2)
            f.screen_Image(220, 620, 300, 450, 'redbox.png')
            box_count = f.image_count('clickplay.png', 'redbox.png', .6)
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
        return True
    else:
        print('Found no login button, login failed')
        return False

def logout():
    # f.find_and_click('logout.png', 'logout_x.png')
    # f.find_and_click('logout.png', 'red_logout.png')
    f.move_mouse(803, 804, 40, 41, True)
    f.move_mouse(715, 716, 700, 701, True)

if __name__ == "__main__":
    login('blah')
    # logout()