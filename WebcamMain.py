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
    
    if rfilt > 255:
        rfilt = 255
    if gfilt > 255:
        gfilt = 255
    if bfilt > 255:
        bfilt = 255
    
    app.RTPfilt.addData(rfilt, gfilt, bfilt)
    logr.append(r)
    logg.append(g)
    logb.append(b)
 

#Log creation    
logr=[]
logg=[]
logb=[]
  
#create instances of camera
camera = webcam2rgbplus.webcam2rgbplus()

#Starting animation and GUI
app = WebcamGUI.CameraGUI(camera,hasData)
ani = animation.FuncAnimation(app.RTPraw.fig, app.RTPraw.update, interval = 100)
ani2 = animation.FuncAnimation(app.RTPfilt.fig, app.RTPfilt.update, interval = 100)

#Filter coefficients
fc = 3 #Cut off frequency of 3Hz
fs = app.camerafps #Sampling rate of camera
f = fc/fs #Normalised frequency
fpy = f*2 #Python normalised frequency

filterorder = 8
dBrejection = 50

#Creating instances of filter
iirfilterr = iir_filter.IIRFilter(signal.cheby2(filterorder, dBrejection, fpy, output = 'sos'))
iirfilterg = iir_filter.IIRFilter(signal.cheby2(filterorder, dBrejection, fpy, output = 'sos'))
iirfilterb = iir_filter.IIRFilter(signal.cheby2(filterorder, dBrejection, fpy, output = 'sos'))

#GUI running
app.mainloop()

loglog = [logr, logg, logb]
np.savetxt("loglog.dat", loglog)

camera.__del__()
app.__del__()