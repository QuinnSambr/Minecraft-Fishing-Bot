import PySimpleGUI as sg
import cv2 
from mss import mss
import numpy as np
from time import time 


def screen():
    layout = [[sg.Text('Persistent window')],      
            [sg.Image(filename='', key='image')],
            [sg.Button('Run Function'), sg.Exit()]]      

    window = sg.Window('Window that stays open', layout)      
    sct = mss()
    mon = {"top": 40, "left": 0, "width": 800, "height": 640}
    while True:
        begin_time = time()
        stream_image = np.array(sct.grab(mon))
        np.shape(stream_image)
                             # The Event Loop
        event, values = window.read()   
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        

        window.FindElement('image').Update(data=stream_image)        

    window.close()


screen()