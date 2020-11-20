# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 21:33:20 2020

@author: ellaw
"""

import WebcamGUI
import matplotlib.animation as animation
import webcam2rgbplus
import numpy as np
    
#create callback method reading camera and plotting in windows
def hasData(retval, data):
    b = data[0]
    g = data[1]
    r = data[2]
    app.RTP.addDatab(b)
    app.RTP.addDatag(g)
    app.RTP.addDatar(r)


   
#create instances of camera
camera = webcam2rgbplus.webcam2rgbplus()
#camera = webcam2rgb.Webcam2rgb()

app = WebcamGUI.CameraGUI(camera,hasData)
ani = animation.FuncAnimation(app.RTP.fig, app.RTP.update, interval = 100)
app.mainloop()

camera.__del__()
