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
import time
    
#create callback method reading camera and plotting in windows
def hasData(retval, data):
    '''Callback method for camera'''
    currenttime = time.time() #Used to identify camera sample rate by printing time of calling
    logtimes.append(currenttime) #Sends previous value to list. List stored in consoletimes.dat at end of program. For analysis run consoletimesanalysis.py

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
    #logr.append(r)
    #logg.append(g)
    #logb.append(b)

#Log creation    
logr=[]
logg=[]
logb=[]
logtimes=[]
  
#create instances of camera
camera = webcam2rgbplus.webcam2rgbplus()

#Starting animation and GUI
app = WebcamGUI.CameraGUI(camera,hasData)
ani = animation.FuncAnimation(app.RTPraw.fig, app.RTPraw.update, interval = 50)
ani2 = animation.FuncAnimation(app.RTPfilt.fig, app.RTPfilt.update, interval = 50)

#Modifiable filter characteristics chosen
filterorder = 10 #Order of filters
fc = 1.75 #Cut off frequency of 3Hz
dBrejection = 50 #Decibell reject at cut off frequency

#Fixed filter characteristics and calculations
fs = app.camerafps #Sampling rate of camera
f = fc/fs #Normalised frequency
fpy = f*2 #Python normalised frequency

#Creating instances of filter
iirfilterr = iir_filter.IIRFilter(signal.cheby2(filterorder, dBrejection, fpy, output = 'sos'))
iirfilterg = iir_filter.IIRFilter(signal.cheby2(filterorder, dBrejection, fpy, output = 'sos'))
iirfilterb = iir_filter.IIRFilter(signal.cheby2(filterorder, dBrejection, fpy, output = 'sos'))

#GUI running
app.mainloop()

loglog = [logr, logg, logb] #Combines r, g and b lists together into one big list to be exported
np.savetxt("loglog.dat", loglog) #Exports the r, g and b big list to loglog.dat file
np.savetxt("consoletimes.dat", logtimes) #Used to check for camera jitter, run consoletimesanalysis.ppy

#Destructors, needed when force closing GUI with camera open
camera.__del__()
app.__del__()