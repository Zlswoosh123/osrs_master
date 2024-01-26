import yaml
import win32gui
import core
import ahk
import pyautogui
import time

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
    worlds = [303,304,305,306,307,310,311,312,313,314,315,317,319,320,321,322,323,
              324,325,327,328,329,331,332,333,334,336,337,338,339,340,341,342,343,344,346,347,348,349,350,351,352,353,
              354,355,356,357,358,359,360,361,362,363,364,366,367,368,369,370,373,374,375,376,377,378,386,
              387,388,389,390,391,395,396,416,420,421,422,423,424,425,428,429,441,443,444,445,446,447,448,
              449,450,459,463,464,465,466,467,474,477,478,479,480,481,482,484,485,486,487,488,489,490,491,492,493,494,
              495,496,505,506,507,508,509,510,511,512,513,514,515,516,517,518,519,520,521,522,523,524,525,526,527,
              528,529,531,532,534,535]
    type = 'clan'
    while True:
        for world in range(len(worlds)-1):
            if type == 'mole':
                value = worlds[world]
                hopmsg = '::hop '+str(value)
                pyautogui.typewrite(hopmsg,.03)
                pyautogui.press('enter')
                time.sleep(15)
                #say message
                molemessage1 = "red: Dont sell mole skins to the GE! Get more from fc: 'MoleBuyer'"
                molemessage2 = "green: Buying all mole skins for 5% over GE price. Save on fees too!"
                molemessage3 = "rainbow:Happy hunting and have fun!"
                pyautogui.typewrite(molemessage1,.03)
                pyautogui.press('enter')
                time.sleep(3)
                pyautogui.typewrite(molemessage2, .03)
                pyautogui.press('enter')
                time.sleep(3)
                pyautogui.typewrite(molemessage3, .03)
                pyautogui.press('enter')
                time.sleep(6)
                #pause
                #world hop
                print(f"Leaving {world}")
            if type == 'ge':
                value = worlds[world]
                hopmsg = '::hop '+str(value)
                pyautogui.typewrite(hopmsg,.03)
                pyautogui.press('enter')
                time.sleep(15)
                #say message
                gemessage1 = "Cash sitting in your bank? Put it to use and make mils per week! [Molebuyer]"
                gemessage2 = "green: Put that cash to work and earn 5% return or more everyday [Molebuyer] fc"
                pyautogui.typewrite(gemessage1,.03)
                pyautogui.press('enter')
                time.sleep(5)
                pyautogui.typewrite(gemessage2, .03)
                pyautogui.press('enter')
                time.sleep(6)
                #pause
                #world hop
                print(f"Leaving {world}")
            if type == 'clan':
                value = worlds[world]
                # hopmsg = '::hop '+str(value)
                # pyautogui.typewrite(hopmsg,.03)
                # pyautogui.press('enter')
                # time.sleep(15)
                #say message
                clanmessage1 = "How it works: I buy mole skins at 5% above GE mid price"
                clanmessage2 = "They can be bought at mid price or even below (not always instant)"
                clanmessage3 = "Below are additional items I buy above GE price:"
                clanmessage4 = "blue/red/black d'hide body (5000/6150/7300), mole claw (8500)"
                clanmessage5 = "Leave offers in GE at margins you decide for easy mils every week"
                pyautogui.typewrite(clanmessage1,.03)
                pyautogui.press('enter')
                time.sleep(3)
                pyautogui.typewrite(clanmessage2, .03)
                pyautogui.press('enter')
                time.sleep(3)
                pyautogui.typewrite(clanmessage3, .03)
                pyautogui.press('enter')
                time.sleep(3)
                pyautogui.typewrite(clanmessage4, .03)
                pyautogui.press('enter')
                time.sleep(3)
                pyautogui.typewrite(clanmessage5, .03)
                pyautogui.press('enter')
                time.sleep(300)
                #pause
                #world hop
                print(f"Leaving {world}")
