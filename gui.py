import PySimpleGUI as sg
import cv2 as cv
import numpy as np
from time import time
from PIL import ImageGrab , Image
from mss import mss
import fishingbot ,multiprocessing , io ,tkinter

#Colour theme of window
sg.theme('DarkGrey2')


def capture_screen():
    """
    Captures images of the pixel postions in monitor and converts into data
    Returns:
        [float]: [the converted data from window capture]
    """
    loop_time = time()
    with mss() as sct:
            monitor = {"top": 40, "left": 0, "width": 800, "height": 640}
    while True:
        # Captures window and converts into numpy array
        window_capture = np.array(sct.grab(monitor))
        # Converts to RGB colour
        window_capture = cv.cvtColor(window_capture, cv.COLOR_RGB2BGR)
        loop_time = time()    
        window_capture = Image.fromarray(window_capture)
        #Keeps the data in memory as buffer
        window_capture_inMemory = io.BytesIO()
        window_capture.save(window_capture_inMemory,format='PNG')
        window_capture_bytes=window_capture_inMemory.getvalue()
        return window_capture_bytes
        
def main():
    """
    Creates a gui with simplegui whilst ingesting and displaying the screen data from view_screen
    """
    # A layout of the window
    layout =[
        [sg.Image(filename='', key='image')],
        [sg.Button('Start Automated Fishing',size=(80,1))],
        [sg.Button('Stop Automated Fishing',button_type='Stop',size=(80,1))],
        [[sg.ReadButton('Exit',size=(80,1))]]
        ]
    #Window title 
    main_window = sg.Window("Automated Minecraft Window", layout, finalize=True,element_justification='c')
    choice = None
    

    while True:
        event, values = main_window._ReadNonBlocking()
        if event is 'Exit' or values is None:
            break 
        elif event is 'Start Automated Fishing':
            # Runs the fishing bot function from the fishingbot_minecraft script
            start_automation = multiprocessing.Process(target=fishingbot.object_detection)
            # Starts multiprocessor
            start_automation.start()
        elif event is 'Stop Automated Fishing':
            #Terminates the multiprocessor function
            start_automation.kill()
            print('Stopped')

        # Update the monitor capture screen every 500ms
        start_image = multiprocessing.Process(target=main_window.find_element('image').Update(data=capture_screen()))
        start_image.start()

    # When Exit event is processed it closes the gui window
    main_window.close()

if __name__ == '__main__':
    main()
