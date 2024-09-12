from threading import Thread
import pywintypes
import win32con
import win32gui
import win32api
import numpy as np
import cv2
import pyautogui as p
import random
import time
import os
import functions
import pytesseract
import core
import yaml
from PIL import Image
from functions import Image_count
from functions import image_Rec_clicker
from functions import screen_Image
from functions import release_drop_item
from functions import drop_item
from functions import Image_to_Text
from functions import invent_crop
from functions import resizeImage
from functions import random_breaks
from functions import image_eel_clicker
from functions import screen_front
from functions import offscreen_mouse
from functions import super_random_breaks
from functions import safe_open, find_and_click
from test import find_object, find_and_click

x, y = find_object(boundaries=[([192, 0, 192], [255, 64, 255])])
if x is not None and y is not None:
    functions.move_mouse(x - 8, x-7, y+1, y+2, click=True, type='right')
# time.sleep(3)