# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 21:33:20 2020

@author: ellaw
"""
#Custom imports
import WebcamGUI
import webcam2rgbplus
import iir_filter 
#Standard imports
import matplotlib.animation as animation
import numpy as np
import scipy.signal as signal
import time
    

def hasData(retval, data):
    '''Callback method for camera'''
    #currenttime = time.time() #Uncomment for jitter checking. Used to identify camera sample rate by printing time of calling. 
    #logtimes.append(currenttime) #Uncomment for jitter checking. Sends previous value to list. List stored in consoletimes.dat at end of program. For analysis run consoletimesanalysis.py

    b = data[0] #Extration of blue value
    g = data[1] #Extraction of green value
    r = data[2] #Extraction of red value
    
    app.RTPraw.addData(r, g, data[0]) #Sends raw data to GUI raw data plot
    rfilt = iirfilterr.filter(r) #Filtering of red value
    gfilt = iirfilterg.filter(g) #Filtering of green value
    bfilt = iirfilterb.filter(b) #Filtering of blue value
    
    #RGB limiting for sake of GUI
    if rfilt > 255: #Check for red limit
        rfilt = 255
    elif rfilt < 0:
        rfilt = 0
    if gfilt > 255: #Check for green limit
        gfilt = 255
    elif gfilt < 0:
        gfilt = 0
    if bfilt > 255: # Check for blue limit
        bfilt = 255
    elif bfilt < 0:
        bfilt = 0
    
    app.RTPfilt.addData(rfilt, gfilt, bfilt) #Sends filtered data to GUI filtered data plot
    #logr.append(r) #Uncomment to log the red value of the camera. Adds the latests raw red value to the list
    #logg.append(g) #Uncomment to log the green value of the camera. Adds the latests raw green value to the list
    #logb.append(b) #Uncomment to log the blue value of the camera. Adds the latests raw blue value to the list


#Log creation    
logr=[] #Creates the red list that stores the red values
logg=[] #Creates the green list that stores the green values
logb=[] #Creates the blue list that stores the blue values
logtimes=[] #Used to store all the times the hasData method is called.
  
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
soscheby = signal.cheby2(filterorder, dBrejection, fpy, output = 'sos')
iirfilterr = iir_filter.IIRFilter(soscheby)
iirfilterg = iir_filter.IIRFilter(soscheby)
iirfilterb = iir_filter.IIRFilter(soscheby)

#GUI running
app.mainloop()

loglog = [logr, logg, logb] #Combines r, g and b lists together into one big list to be exported
np.savetxt("loglog.dat", loglog) #Exports the r, g and b big list to loglog.dat file
np.savetxt("consoletimes.dat", logtimes) #Exports logtimes to consoletimes.dat. For analysis run consoletimesanalysis.ppy

#Destructors, needed when force closing GUI with camera open
camera.__del__()
app.__del__()