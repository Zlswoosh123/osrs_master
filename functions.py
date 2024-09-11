import config_generator
import core
import math
import numpy as np
import cv2
import pyautogui
import random
import time
from shapely.geometry import Polygon
import ctypes
import yaml
from PIL import Image, ImageGrab
import os
import platform
import win32gui

# Vars
global hwnd
hwnd = 0
global iflag
global icoord
iflag = False
global newTime_break
newTime_break = False
global timer
global timer_break
global ibreak
runelite = 'RuneLite'
window = 1
fish_type = 'infernal_eel'
import pytesseract

with open("pybot-config.yaml", "r") as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)


class bcolors:
    OK = '\033[92m'  # GREEN
    WARNING = '\033[93m'  # YELLOW
    FAIL = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET COLOR


with open("pybot-config.yaml", "r") as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)

pytesseract.pytesseract.tesseract_cmd = data[0]['Config']['tesseract_path'] + "tesseract"
try:
    im = Image.open("images/tynan_shop.png")
    text = pytesseract.image_to_string(im)
    print(bcolors.OK + "Testing Tesseract is configured: Passed |", text)
except:
    pass
os.environ["TESSDATA_PREFIX"] = data[0]['Config']['tesseract_path']  # + "tessdata"
try:
    im = Image.open("images/tynan_shop.png")
    text = pytesseract.image_to_string(im)
    print(bcolors.OK + "Testing Tesseract is configured: Passed |", text)
except:
    os.environ["TESSDATA_PREFIX"] = data[0]['Config']['tesseract_path'] + "tessdata"
    try:
        im = Image.open("images/tynan_shop.png")
        text = pytesseract.image_to_string(im)
        print(bcolors.OK + "Testing Tesseract is configured: Passed |", text)
    except:
        print(
            bcolors.FAIL + "Error setting up tesseract: Check the pyconfig.yaml is set up to your tesseract path or is installed correctly, go here and install latest version: " + 'https://digi.bib.uni-mannheim.de/tesseract/?C=M;O=D')

# Constants
gdi32 = ctypes.WinDLL('gdi32.dll')

VERTRES = 10
DESKTOPVERTRES = 117

inventory_spots = [
    (650, 660, 498, 505),  # Spot 1
    (693, 703, 498, 505),  # Spot 2
    (736, 746, 498, 505),  # Spot 3
    (779, 789, 498, 505),  # Spot 4
    (650, 660, 533, 540),  # Spot 5
    (693, 703, 533, 540),  # Spot 6
    (736, 746, 533, 540),  # Spot 7
    (779, 789, 533, 540),  # Spot 8
    (650, 660, 568, 575),  # Spot 9
    (693, 703, 568, 575),  # Spot 10
    (736, 746, 568, 575),  # Spot 11
    (779, 789, 568, 575),  # Spot 12
    (650, 660, 603, 610),  # Spot 13
    (693, 703, 603, 610),  # Spot 14
    (736, 746, 603, 610),  # Spot 15
    (779, 789, 603, 610),  # Spot 16
    (650, 660, 638, 645),  # Spot 17
    (693, 703, 638, 645),  # Spot 18
    (736, 746, 638, 645),  # Spot 19
    (779, 789, 638, 645),  # Spot 20
    (650, 660, 673, 680),  # Spot 21
    (693, 703, 673, 680),  # Spot 22
    (736, 746, 673, 680),  # Spot 23
    (779, 789, 673, 680),  # Spot 24
    (650, 660, 708, 715),  # Spot 25
    (693, 703, 708, 715),  # Spot 26
    (736, 746, 708, 715),  # Spot 27
    (779, 789, 708, 715),  # Spot 28
]


def click_object():
    # 3rd item
    # d = random.uniform(0.11, 0.18)
    # time.sleep(d)
    pyautogui.click()
    print('clicked something')


def move_mouse(x1, x2, y1, y2, b=0, click = True):
    if b == 0:
        b = random.uniform(0.05, 0.25)
    x_move = random.randrange(x1, x2) - 4
    y_move = random.randrange(y1, y2) - 4
    pyautogui.moveTo(x_move, y_move, duration=b)
    if click == True:
        pyautogui.click()


class DeviceCap:
    VERTRES = 10
    DESKTOPVERTRES = 117


def get_scaling_factor():
    gdi32 = ctypes.WinDLL('gdi32.dll')

    # Get the screen's device context (DC)
    desktop = gdi32.CreateDCW('DISPLAY', None, None, None)

    # Get the logical and physical screen height
    logical_screen_height = gdi32.GetDeviceCaps(desktop, DeviceCap.VERTRES)
    physical_screen_height = gdi32.GetDeviceCaps(desktop, DeviceCap.DESKTOPVERTRES)

    # Calculate the scaling factor
    scaling_factor = physical_screen_height / logical_screen_height

    return scaling_factor


# Usage
scaling_factor = get_scaling_factor()
if scaling_factor == 1.0:
    print(bcolors.OK + "Scaling Factor:", scaling_factor * 100, "%")
else:
    print(bcolors.FAIL + "Scaling Factor: Failed set to 100% | Actual:", scaling_factor * 100, "%")


def get_os_configuration():
    # Get scale and layout information
    user32 = ctypes.windll.user32
    scale_factor = user32.GetDpiForSystem()

    # Get font size information
    scale = 96 / scale_factor
    font_size = user32.SystemParametersInfoW(0x0030, 0, 0, 0) / scale  # SPI_GETNONCLIENTMETRICS

    # Get display resolution information
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)

    return scale_factor, font_size, width, height


def offscreen_mouse():
    print('Starting offscreen_mouse')
    xcoord = random.uniform(925, 1200)
    ycoord = random.uniform(1000, 170)
    new_coord = (xcoord, ycoord)
    min, max = random.uniform(0.1, .25), random.uniform(0.35, .7)
    b = random.uniform(min, max)
    print('Trying to move to coord offscreen!')
    pyautogui.moveTo(new_coord, duration=b)


def double_random(min, max, scaler=.5):
    min = random.uniform(min * scaler, min * (1 + scaler))
    max = random.uniform(max * scaler, max * (1 + scaler))
    if min > max:
        min, max = max, min
    wait = random.uniform(min, max)
    return wait


def super_random_breaks(a, b, c, d):
    min1 = random.uniform(a, b)  # e.g. 1-3
    max1 = random.uniform(c, d)  # e.g. 5-7
    if min1 > max1:
        min1, max1 = max1, min1
    wait = random.uniform(min1, max1)  # e.g 2, 6
    return wait


def safe_open(image, png):
    # print('Starting safe_open')
    count = 0
    while image is None and count < 5:
        image = cv2.imread('C:/Users/Zlswo/PycharmProjects/osrs_master/images/' + png)
        print(f'Sleeping until image is created')
        time.sleep(2)
        count += 1
    if count == 5:
        print('Safe open failed!')
        return image
    return image


def screen_front(runelite):
    print('Starting screen_front')
    try:
        pyautogui.keyUp('shift')
        window = win32gui.FindWindow(None, runelite)
        win32gui.ShowWindow(window, 5)
        win32gui.SetForegroundWindow(window)  # Set it as the foreground window
        win32gui.SetActiveWindow(window)
    except Exception as err:
        print(f"An exception occurred: {err}")
        time.sleep(7)


# Usage
scale_factor, font_size, width, height = get_os_configuration()

if width == 1920 and height == 1080:
    print(bcolors.OK + "Resolution:", width, "x", height)
else:
    print(bcolors.FAIL + "Resolution not set correctly: Failed set to 1920 x 1080 | Actual:", width, "x", height)
try:
    print(bcolors.OK + "tesseract version:", pytesseract.get_tesseract_version())
except SystemExit:
    print(bcolors.FAIL + "tesseract version detailed: not found")

print(bcolors.RESET)
filename = data[0]['Config']['pc_profile']

osrs = data[0]['Config']['file_path_to_client']

live_file = "jagex_cl_oldschool_LIVE.dat"

random_file = "random.dat"
try:
    os.remove(filename + osrs + live_file)
    os.remove(filename + osrs + random_file)
except OSError:
    pass
except FileNotFoundError:
    pass

if platform.system() == 'Linux' or platform.system() == 'Mac':
    filename = filename + osrs + "/jagexcache/oldschool/LIVE/"
else:
    filename = filename + osrs + "\\jagexcache\\oldschool\\LIVE\\"

try:
    for f in os.listdir(filename):
        try:
            if not f.startswith("main_file"):
                continue
            os.remove(os.path.join(filename, f))
        except OSError:
            pass
        except FileNotFoundError:
            pass

except OSError:
    pass
except FileNotFoundError:
    pass
#
print('jagex files deleted')


def deposit_all_Bank():
    print('Starting deposit_all_Bank')
    banker = 50
    b = random.uniform(0.1, 0.77)
    x = random.randrange(480, 500)  # x = random.randrange(1040, 1050)
    y = random.randrange(626, 647)  # y = random.randrange(775, 805)
    pyautogui.moveTo(x, y, duration=b)
    b = random.uniform(0.01, 0.1)
    pyautogui.click(x, y, duration=b, button='left')
    c = random.uniform(0.1, 4.5)
    time.sleep(c)


def invent_crop():  # Takes picture of inventory
    print('Starting invent_crop')
    global window
    screen_Image(620, 820, 460, 780, 'inventshot.png')


def resize_quick():
    print('Starting resize_quick')
    left = 30
    top = 49
    right = 113
    bottom = 70
    screen_Image(left, right, top, bottom, 'screen_resize.png')
    # print('Taking screen_resize.png!')


def resize_quick_combat(l=30, t=49, r=113, b=68, image='screen_resize.png'):
    # print('Starting resize_quick_combat')
    # left = 30
    # top = 49
    # right = 113
    # bottom = 68
    left = l
    top = t
    right = r
    bottom = b
    # left, top, right, bottom = rand_size(left, top, right, bottom)
    # print(f'resize values: {left}, {top}, {right}, {bottom}')
    screen_Image(left, right, top, bottom, 'screen_resize.png')
    # print('Taking screen_resize.png!')


def resizeImage(image='screen_resize.png'):
    # print('Starting resizeImage -- See resize_quick')
    resize_quick()
    png = 'images/' + image
    im = Image.open(png)
    # saves new cropped image
    width, height = im.size
    new_size = (width * 7, height * 7)
    im1 = im.resize(new_size)
    # print('Taking textshot.png!')
    im1.save(f'images/{image}_enhanced.png')


def Miner_Image_quick():
    print('Starting miner_image_quick')
    left = 0
    top = 0
    right = 865
    bottom = 830

    im = ImageGrab.grab(bbox=(left, top, right, bottom))
    im.save('images/miner_img.png', 'png')


def Image_to_Text(preprocess, image, parse_config='--psm 7'):
    # print('Starting image_to_text')
    resizeImage(image)
    change_brown_black()
    # construct the argument parse and parse the arguments
    image = cv2.imread('images/' + image)
    image = cv2.bitwise_not(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # check to see if we should apply thresholding to preprocess the
    # image
    if preprocess == "thresh":
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # make a check to see if median blurring should be done to remove
    # noise
    if preprocess == "blur":
        gray = cv2.medianBlur(gray, 3)

    if preprocess == 'adaptive':
        gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)
    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    with Image.open(filename) as im:
        text = pytesseract.image_to_string(im, config=parse_config)
    os.remove(filename)
    # print(text)
    return text


def resizeImage_combat(image, new_image='textshot.png'):
    # print('Starting resizeImage_combat -- See resize_quick')
    resize_quick_combat(image)
    png = 'images/' + image
    im = Image.open(png)
    # saves new cropped image
    width, height = im.size
    new_size = (width * 4, height * 4)
    im1 = im.resize(new_size)
    # print('Taking textshot.png!')
    im1.save('images/' + new_image)


def Image_to_Text_combat(preprocess, image, parse_config='--psm 7'):
    print('Starting image_to_text')
    # resizeImage_combat(image=image, new_image='textshot.png')
    # change_brown_black()
    # construct the argument parse and parse the arguments
    image = cv2.imread('images/' + image)
    image = cv2.bitwise_not(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  #
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # check to see if we should apply thresholding to preprocess the
    # image
    if preprocess == "thresh":
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # make a check to see if median blurring should be done to remove
    # noise
    if preprocess == "blur":
        gray = cv2.medianBlur(gray, 3)

    if preprocess == 'adaptive':
        gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)
    # print(f'Filename is {filename}')
    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    with Image.open(filename) as im:
        text = pytesseract.image_to_string(im, config=parse_config)
        # print(f'Text from image_to_text is: {text}')
    try:
        os.remove(filename)
    except:
        print(f'File {filename} not found, skipping!')
    # print(f'Filename after remove is {filename}')
    # print(text)
    time.sleep(random.uniform(.5, 1))
    return text


def screen_Image_new(name='screenshot.png'):
    # print('Starting screen_image_new')
    x, y, w, h = core.getWindow(data[0]['Config']['client_title'])
    im = ImageGrab.grab(bbox=(x, y, x + w, y + h))
    im.save('images/' + name, 'png')


def screen_Image(left=0, right=800, top=0, bottom=800, name='screenshot.png'):  # Takes image and gives a name
    # print('Starting screen_image')
    myScreenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    width, height = myScreenshot.size  # Assuming myScreenshot is a PIL Image object
    print('About to screenshot.save')
    myScreenshot.save('C:/Users/Zlswo/PycharmProjects/osrs_master/images/' + name)
    print(f"Screenshot size: {myScreenshot.size}")
    print(f"Saving region: left={left}, top={top}, right={right}, bottom={bottom}")
    assert 0 <= left < right, "Invalid horizontal coordinates"
    assert 0 <= top < bottom, "Invalid vertical coordinates"


def screen_block(image):
    image = cv2.rectangle(image, pt1=(540, 250), pt2=(800, 0), color=(0, 0, 0), thickness=-1)  # blocks map
    image = cv2.rectangle(image, pt1=(0, 650), pt2=(800, 800), color=(0, 0, 0), thickness=-1)  # blocks chat
    image = cv2.rectangle(image, pt1=(605, 450), pt2=(800, 800), color=(0, 0, 0), thickness=-1)  # blocks inventory
    return image


def change_brown_black():
    # Load the aerial image and convert to HSV colourspace
    image = cv2.imread("images/textshot.png")
    safe_open(image, 'textshot.png')
    # hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # define the list of boundaries
    # BGR
    # Define lower and uppper limits of what we call "brown"
    brown_lo = np.array([0, 0, 0])
    brown_hi = np.array([60, 80, 85])

    # Mask image to only select browns
    mask = cv2.inRange(image, brown_lo, brown_hi)

    # Change image to red where we found brown
    image[mask > 0] = (0, 0, 0)

    cv2.imwrite("images/textshot.png", image)


def McropImage_quick():
    print('Starting mcropimage_quick')
    left = 0
    top = 0
    right = 800
    bottom = 800

    im = ImageGrab.grab(bbox=(left, top, right, bottom))
    im.save('images/screenshot2.png', 'png')


#
#
def findarea_attack_quick(object, deep=8):
    print('Starting findarea_attack_quick')
    McropImage_quick()

    image = cv2.imread(r"images/screenshot2.png")
    screen_block(image)

    # B, G, R
    # --------------------- ADD OBJECTS -------------------
    red = ([0, 0, 180], [80, 80, 255])
    green = ([0, 180, 0], [80, 255, 80])
    pickup_high = ([200, 0, 100], [255, 30, 190])
    attack_blue = ([250, 250, 0], [255, 255, 5])
    amber = ([0, 160, 160], [80, 255, 255])
    # --------------------- ADD OBJECTS -------------------
    ore_list = [red, green, pickup_high, attack_blue, amber]
    boundaries = [ore_list[object]]
    # loop over the boundaries
    for (lower, upper) in boundaries:
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")
        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(image, lower, upper)
        # output = cv2.bitwise_and(image, image, mask=mask)
        ret, thresh = cv2.threshold(mask, 40, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) != 0:
            # draw in blue the contours that were found
            # cv2.drawContours(output, contours, -1, 255, 3)
            # find the biggest countour (c) by the area
            c = max(contours, key=cv2.contourArea)

            x, y, w, h = cv2.boundingRect(c)
            # draw the biggest contour (c) in green
            whalf = max(round(w / 2), 1)
            hhalf = max(round(h / 2), 1)
            # cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
            x = random.randrange(x + whalf - deep, x + max(whalf + deep, 1))  # 950,960
            # print('attack x: ', x)
            y = random.randrange(y + hhalf - deep, y + max(hhalf + deep, 1))  # 490,500
            # print('attack y: ', y)
            b = random.uniform(0.05, 0.15)
            # print(f'hhalf is: {hhalf}')
            # print(f'deep is: {deep}')
            # print(f'x is: {x}')
            # print(f'y is: {y}')
            pyautogui.moveTo(x, y, duration=b)
            b = random.uniform(0.02, 0.08)
            pyautogui.click(duration=b)
            return (x, y)
    return (0, 0)
    # show the images
    # cv2.imshow("Result", np.hstack([image, output]))


def invent_enabled():
    return Image_count('inventory_enabled.png', threshold=0.95)


def run_enabled():
    return Image_count('run_enabled.png', threshold=0.95)


def make_enabled(make='make_craft.png'):
    return Image_count(make, threshold=0.95)


def image_Rec_clicker(image, object, iheight=5, iwidth=2, threshold=0.8, clicker='left', ispace=25, playarea=True,
                      fast=False):
    print('Starting image_Rec_clicker')
    global icoord
    global iflag
    # Update images, convert to gray, match template, apply threshold
    img_rgb = cv2.imread('images/' + image)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('images/' + object, 0)
    w, h = template.shape[::-1]
    pt = None
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    print(f'res is: {res}')
    iflag = False

    # for image where template match % > threshold
    for pt in zip(*loc[::-1]):
        # print('Starting our for loop in zip now!')
        # print(f'Current pt is {pt}')
        resizeImage()  # update screenresize/text images
        invent_crop()  # update inventory.png
        # confirm how below draws rectangles
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        if pt is None:
            iflag = False
            print('pt is None so iflag is False')
        else:
            # useless?
            cropx = 620
            cropy = 457
            iflag = True
            # i vars are constants todo add double randomness
            x = random.randrange(iwidth, iwidth + ispace)  # + cropx
            y = random.randrange(iheight, iheight + ispace)  # + cropy
            icoord = pt[0] + iheight + x
            icoord = (icoord, pt[1] + iwidth + y)
            b = super_random_breaks(.03, .12, .14, .25)
            print('Trying to move to coord in rec_clicker!')
            pyautogui.moveTo(icoord, duration=b)
            b = super_random_breaks(.03, .12, .14, .25)
            print('Trying to click coord!')
            pyautogui.keyDown('shift')
            pyautogui.click(icoord, duration=b, button=clicker)
    print('Ending image_Rec_clicker')
    return iflag


def bank_item_clicker(image, iheight=5, iwidth=2, threshold=0.8, clicker='left', ispace=25):
    print('Starting bank_clicker')
    global icoord
    global iflag
    # Update images, convert to gray, match template, apply threshold
    img_rgb = cv2.imread('images/screenshot.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('images/' + image, 0)
    w, h = template.shape[::-1]
    pt = None
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    print(f'res is: {res}')
    iflag = False

    # for image where template match % > threshold
    for pt in zip(*loc[0:1:-1]):
        # print('Starting our for loop in zip now!')
        # print(f'Current pt is {pt}')
        resizeImage()  # update screenresize/text images
        invent_crop()  # update inventory.png
        # confirm how below draws rectangles
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        if pt is None:
            iflag = False
            print('pt is None so iflag is False')
        else:
            # useless?
            cropx = 620
            cropy = 457
            iflag = True
            # i vars are constants todo add double randomness
            x = random.randrange(iwidth, iwidth + ispace) + cropx
            y = random.randrange(iheight, iheight + ispace) + cropy
            icoord = pt[0] + iheight + x
            icoord = (icoord, pt[1] + iwidth + y)
            b = super_random_breaks(.03, .12, .14, .25)
            print('Trying to move to coord in rec_clicker!')
            pyautogui.moveTo(icoord, duration=b)
            b = super_random_breaks(.03, .12, .14, .25)
            print('Trying to click coord!')
            pyautogui.click(icoord, duration=b, button=clicker)
    print('Ending image_Rec_clicker')
    return iflag


def image_eel_clicker(image, event, iheight=5, iwidth=2, threshold=0.8, clicker='left', ispace=8, playarea=True,
                      fast=False):
    print(f'Starting image_eel_clicker for {image}')
    global icoord
    global iflag
    global runelite
    loop_end = 0
    invent_crop()
    img_rgb = cv2.imread('images/inventshot.png')
    safe_open(img_rgb, 'inventshot.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('images/' + image, 0)
    safe_open(template, image)
    w, h = template.shape[::-1]
    pt = None
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    iflag = False
    print('Starting for loop in eel_clicker!')
    for pt in zip(*loc[::-1]):
        whalf = max(round(w / 2), 1)
        hhalf = max(round(h / 2), 1)
        cv2.rectangle(img_rgb, pt, (pt[0] + whalf, pt[1] + hhalf), (0, 0, 255), 2)
        # Adding logic to skip the loop, remove?
        cropx = 620
        cropy = 480
        x = random.randrange(iwidth, iwidth + ispace) + cropx
        y = random.randrange(iheight, iheight + ispace) + cropy
        icoord = pt[0] + iheight + x
        icoord = (icoord, pt[1] + iwidth + y)
        b = super_random_breaks(.03, .12, .14, .25)
        print('Trying to move to coord in rec_clicker!')
        pyautogui.moveTo(icoord, duration=b)
        b = super_random_breaks(.03, .12, .14, .25)
        print('Trying to click coord!')
        pyautogui.click(icoord, duration=b, button=clicker)
        return iflag


def Image_count(object, threshold=0.8, left=0, top=0, right=865, bottom=830):
    # Window 1: object, threshold=0.8, left=0, top=0, right=0, bottom=0
    # Window 2: object, threshold=0.88, left=1000, top=0, right=1920, bottom=800
    counter = 0
    screen_Image(left, right, top, bottom, name='screenshot.png')
    invent_crop()
    img_rgb = cv2.imread('images/inventshot.png')
    safe_open(img_rgb, 'inventshot.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('images/' + object, 0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        counter += 1
    return counter


def invent_count(object, threshold=0.7):
    global window
    print(f'Starting invent_count')
    invent_crop()
    counter = 0
    img_rgb = cv2.imread('images/inventshot.png')
    safe_open(img_rgb, 'inventshot.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('images/' + object, 0)
    safe_open(template, object)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    # print(f'res is {res}')
    loc = np.where(res >= threshold)
    # print(f'loc is {loc}')
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        counter += 1
    return counter


def image_count(object, image, threshold=0.7):  # counts how many objects in image
    global window
    print(f'Starting image_count')
    counter = 0
    img_rgb = cv2.imread('images/' + image)
    safe_open(img_rgb, object)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('images/' + object, 0)
    safe_open(template, object)
    # print(f'template is {template}')
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    # res = cv2.matchTemplate(img_gray, template, cv2.TM_SQDIFF_NORMED)
    # print(f'res is {res}')
    loc = np.where(res >= threshold)
    # print(f'loc is {loc}')
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        counter += 1
    return counter


def move_mouse(x1, x2, y1, y2, click=False):
    b = random.uniform(0.15, 0.45)
    x_move = random.randrange(x1, x2) - 4
    y_move = random.randrange(y1, y2) - 4
    pyautogui.moveTo(x_move, y_move, duration=b)
    if click:
        pyautogui.click()


def drop_item():
    print('Starting drop_item!')
    pyautogui.keyUp('shift')
    c = random.uniform(0.1, 0.2)
    d = random.uniform(0.1, 0.23)

    time.sleep(c)
    pyautogui.keyDown('shift')
    time.sleep(d)
    print('Ending drop_item!')

def click_row(row_counter):
    print('Abs start')
    pyautogui.press('f1')
    pyautogui.press('esc')
    row = (row_counter * 4)
    for i in range(row, row+4):
        move_mouse(*inventory_spots[i], True)
    print('Abs end')

def release_drop_item():
    e = random.uniform(0.1, 0.3)
    f = random.uniform(0.1, 0.2)

    time.sleep(e)
    pyautogui.keyUp('shift')
    pyautogui.press('shift')
    time.sleep(f)


def random_breaks(minsec, maxsec):
    e = random.uniform(minsec, maxsec)
    time.sleep(e)


def super_random_breaks(a, b, c, d):
    min1 = random.uniform(a, b)  # e.g. 1-3
    max1 = random.uniform(c, d)  # e.g. 5-7
    wait = random.uniform(min1, max1)  # e.g 2, 6
    return wait


def find_and_click(image='screenshot.png', object='item.png', x1=0, x2=900, y1=0, y2=900,
                   iheight=4, iwidth=4, threshold=0.8, clicker='left', ispace=10, num_objects=1):
    counter = 0
    # screen_Image(left=x1, right=x2, top=y1, bottom=y2, name=image)
    global icoord
    global iflag
    # Update images, convert to gray, match template, apply threshold
    img_rgb = cv2.imread('images/' + image)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('images/' + object, 0)
    w, h = template.shape[::-1]
    pt = None
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    # print(f'res is: {res}')
    iflag = False

    # for image where template match % > threshold
    for pt in zip(*loc[::-1]):
        # print('Starting our for loop in zip now!')
        # print(f'Current pt is {pt}')
        # resizeImage()  # update screenresize/text images
        # invent_crop()  # update inventory.png
        # confirm how below draws rectangles
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        if pt is None:
            iflag = False
            print('pt is None so iflag is False')
        else:
            # useless?
            cropx = 620
            cropy = 457
            iflag = True
            # i vars are constants
            x = random.randrange(iwidth, iwidth + ispace)  # + cropx
            y = random.randrange(iheight, iheight + ispace)  # + cropy
            icoord = pt[0] + x
            icoord = (icoord, pt[1] + y)  # + y in the ()
            b = super_random_breaks(.03, .12, .14, .25)
            print('Trying to move to coord in rec_clicker!')
            pyautogui.moveTo(icoord, duration=b)
            b = super_random_breaks(.03, .12, .14, .25)
            print('Trying to click coord!')
            pyautogui.click(icoord, duration=b, button=clicker)
            counter += 1
            if counter >= num_objects:
                return True
    print('Ending image_Rec_clicker')
    return False


def findarea(object):
    screen_Image()
    image = cv2.imread('images/screenshot.png')
    red = ([0, 0, 180], [80, 80, 255])  # 0 Index
    green = ([0, 180, 0], [80, 255, 80])  # 1 Index
    amber = ([0, 200, 200], [60, 255, 255])  # 2 Index
    pickup_high = ([250, 0, 167], [255, 5, 172])  # 3 Index
    attack_blue = ([250, 250, 0], [255, 255, 5])
    object_list = [red, green, amber, pickup_high, attack_blue]
    boundaries = [object_list[object]]
    # loop over the boundaries
    for (lower, upper) in boundaries:
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")
        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(image, lower, upper)
        output = cv2.bitwise_and(image, image, mask=mask)
        ret, thresh = cv2.threshold(mask, 40, 255, 0)
        # if (cv2.__version__[0] > 3):
        # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # else:
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        # draw in blue the contours that were founded
        cv2.drawContours(output, contours, -1, 255, 3)
        # find the biggest countour (c) by the area
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        # draw the biggest co  ntour (c) in green
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # show the images
    cv2.imshow("Result", np.hstack([image, output]))
    cv2.waitKey(0)
