# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 21:33:20 2020

@author: ellaw
"""

import WebcamGUI
import matplotlib.animation as animation
import webcam2rgbplus
import iir_filter 
import numpy as np
    
#create callback method reading camera and plotting in windows
def hasData(retval, data):
    b = data[0]
    g = data[1]
    r = data[2]
    app.RTPraw.addDatab(b)
    app.RTPraw.addDatag(g)
    app.RTPraw.addDatar(r)
    
    rfilt, gfilt, bfilt = iirfilter.filt3(r,g,b)
    
    app.RTPfilt.addDatab(b)
    app.RTPfilt.addDatag(g)
    app.RTPfilt.addDatar(r)

   
#create instances of camera
camera = webcam2rgbplus.webcam2rgbplus()
#camera = webcam2rgb.Webcam2rgb()

r = 0.2
f = 0
w = 2*np.pi*f 
iirfilter = iir_filter.IIR_filter(r,w)

app = WebcamGUI.CameraGUI(camera,hasData)
ani = animation.FuncAnimation(app.RTPraw.fig, app.RTPraw.update, interval = 100)
ani2 = animation.FuncAnimation(app.RTPfilt.fig, app.RTPfilt.update, interval = 100)
app.mainloop()

camera.__del__()
