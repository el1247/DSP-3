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
import scipy.signal as signal
    
#create callback method reading camera and plotting in windows
def hasData(retval, data):
    b = data[0]
    g = data[1]
    r = data[2]
    app.RTPraw.addData(r, g, b)
    rfilt = iirfilterr.filter(r)
    gfilt = iirfilterg.filter(g)
    bfilt = iirfilterb.filter(b)
    app.RTPfilt.addData(rfilt, gfilt, bfilt)
    
  
#create instances of camera
camera = webcam2rgbplus.webcam2rgbplus()

#Filter coefficients
fc = 5 #Cut off frequency of 5Hz
fs = 30 #Sampling rate of 30 Hz #Move this to tested value somehow?
f = fc/fs #Normalised frequency
fpy = f*2 #Python normalised frequency

filterorder = 7
dBrejection = 50

iirfilterr = iir_filter.IIRFilter(signal.cheby2(filterorder, dBrejection, fpy, output = 'sos'))
iirfilterg = iir_filter.IIRFilter(signal.cheby2(filterorder, dBrejection, fpy, output = 'sos'))
iirfilterb = iir_filter.IIRFilter(signal.cheby2(filterorder, dBrejection, fpy, output = 'sos'))

#Starting animation and GUI
app = WebcamGUI.CameraGUI(camera,hasData)
ani = animation.FuncAnimation(app.RTPraw.fig, app.RTPraw.update, interval = 100)
ani2 = animation.FuncAnimation(app.RTPfilt.fig, app.RTPfilt.update, interval = 100)
app.mainloop()

camera.__del__()
