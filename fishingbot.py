import cv2
from PIL import Image,ImageGrab
import numpy as np 
from mss import mss
from time import time 
from time import sleep
import pyautogui
import pydirectinput


def casting(kb):
    sleep(5)
    kb.keyDown('c')
    sleep(1)
    kb.rightClick()
    sleep(2)


def reel(temp,prev_loc,kb):
    """
    Find the difference from the current and previous position and compares the difference
    Args:
        temp ([float]): current position of the bobber
        prev_loc ([float]): previous position of the bobber
    """
    if temp - prev_loc >= 20:
        sleep(0.5)
        kb.rightClick()
        sleep(0.5)
        kb.rightClick()
        sleep(1.5)

def object_detection():
    keyboard_input = pydirectinput 
    # Window position and res being captured
    mon = {'top': 100, 'left':200, 'width':600, 'height':480}
    sct = mss()
    print("Ready")
    casting(keyboard_input)


    # Tempate Matching image to be compared
    bobber_input = cv2.imread('bobber.png', cv2.IMREAD_UNCHANGED)

    # Current Position of Height and Width 
    w = bobber_input.shape[1]
    h = bobber_input.shape[0]

    # Arbitrary previous value for initialization
    prev_loc=999

    while True:
        """
        Loop treats the screen capture function as a live display capture ,refreshing 24 times a second
        """
        x=''
        # begin_time = time()
        minecraft_input = np.array(sct.grab(mon))
        
        # Open CV tempate matching function
        detection_output = cv2.matchTemplate(minecraft_input, bobber_input, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(detection_output)

        # Assigning temp current position
        temp = max_loc[1]
        # Comparing Previous Value to Temp Value
        if prev_loc ==999:
            prev_loc = temp      
            continue

        # If the detection determines the accuracy of the match is above 60% then draw bounding box and label the cords
        if max_val >= 0.60:
            # Bobber Bounding Box and Cords
            cv2.rectangle(minecraft_input, max_loc, (max_loc[0] + w, max_loc[1] + h), (0,255,255), 2)
            cv2.putText(minecraft_input, str(max_loc), (max_loc[0] + w, max_loc[1] + h), cv2.FONT_HERSHEY_SIMPLEX ,1,(0,255,255))
            reel(temp,prev_loc,keyboard_input)
            prev_loc = temp



