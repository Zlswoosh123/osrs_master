import yaml
import win32gui
import core
import ahk
import pyautogui
import time
import functions2 as f2

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
    print(BaseException)
    pass

try:
    x_win, y_win, w_win, h_win = core.getWindow(data[0]['Config']['client_title'])
except BaseException:
    print("Unable to find window:", data[0]['Config']['client_title'], "| Please see list of window names below:")
    core.printWindows()
    print(BaseException)
    pass

if __name__ == "__main__":
    worlds = f2.worlds_us
    type = 'main'
    running = True
    while running:
        for world in range(len(worlds)-1):
            if type == 'main':
                value = worlds[world]
                hopmsg = '::hop '+str(value)
                pyautogui.typewrite(hopmsg,.03)
                pyautogui.press('enter')
                time.sleep(15)
                #say message
                mainmessage1 = "Yoyo bankstanding people, I bring new music to grind to for the interested"
                mainmessage2 = "I produce the music myself and its actually solid if you like the genre"
                mainmessage3 = "For EDM Fans here, checkout 'Fire in the Sound - Songs of Siren' (all platforms)"
                mainmessage4 = "Much love for any subs if you enjoy the music. Ty for the time and gl grinding"
                pyautogui.typewrite(mainmessage1,.03)
                pyautogui.press('enter')
                time.sleep(3)
                pyautogui.typewrite(mainmessage2, .03)
                pyautogui.press('enter')
                time.sleep(3)
                pyautogui.typewrite(mainmessage3, .03)
                pyautogui.press('enter')
                time.sleep(3)
                pyautogui.typewrite(mainmessage4, .03)
                pyautogui.press('enter')
                f2.random_wait(16, 24)
                #pause
                #world hop
                print(f"Leaving {world}")
            # if type == 'side':
            #     value = worlds[world]
            #     hopmsg = '::hop '+str(value)
            #     pyautogui.typewrite(hopmsg,.03)
            #     pyautogui.press('enter')
            #     time.sleep(15)
            #     #say message
            #     sidemessage1 = "I've been enjoying listening to solid lofi while I grind"
            #     sidemessage2 = ""
            #     pyautogui.typewrite(sidemessage1,.03)
            #     pyautogui.press('enter')
            #     time.sleep(5)
            #     pyautogui.typewrite(sidemessage2, .03)
            #     pyautogui.press('enter')
            #     time.sleep(6)
            #     #pause
            #     #world hop
            #     print(f"Leaving {world}")
        running = False

