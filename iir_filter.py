# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 16:31:47 2020

@author: ellaw
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

'''Todo: consider switching to fixed point arithmetic (+14 or +30) as dealing with integers. Only need to scale coefficients?'''

class IIR2Filter():
    '''2nd order IIR filter'''
    def __init__(self,_coefficients):
        '''Initializer. Takes in filter coefficients in constructor'''
        self.b0 = _coefficients[0]
        self.b1 = _coefficients[1]
        self.b2 = _coefficients[2]
        self.a0 = _coefficients[3]
        self.a1 = _coefficients[4]
        self.a2 = _coefficients[5]
        
        #Form 2 buffers
        self.buffer1 = 0
        self.buffer2 = 0
        

    def filter(self, x):
        '''Filter function. Takes in scalar x and returns scalar y. It has 2 accumulator 2 delays.'''
        lhsadder = x - self.buffer1*self.a1 - self.buffer2*self.a2
        rhsadder = lhsadder*self.b0 + self.buffer1*self.b1 + self.buffer2*self.b2
        self.buffer2 = self.buffer1
        self.buffer1 = lhsadder
        return rhsadder



class IIRFilter():
    '''Chain of second order filters created by IIR2Filter'''
    def __init__(self, sosarray):
        self.IIR2Farray = []
        self.order = int(len(sosarray))
        for i in range(self.order):
            self.IIR2Farray.append(IIR2Filter(sosarray[i]))


    def filter(self, x):
        '''Filter function for class. Takes in a scalar x and returns scalar y, which has been filtered through all arrays in self.IIR2Farray'''
        for i in self.IIR2Farray:
            x = i.filter(x)    
        return x



#Start of main
if __name__ == '__main__':
    #Modifiable filter characteristics
    filtorder = 10 #order of filter
    fc = 1.75 #cut off frequency
    dBrej = 50 #dB rejection of the stop band
    
    #Fixed filter characteristics and calculations
    fs = 15 #sampling frequency
    f = fc/fs #normalised frequency
    fpy = f*2 #python normalised frequency
    
    #Coefficient and filter creation
    b_c2, a_c2 = signal.cheby2(filtorder, dBrej, fpy)
    cheb2 = signal.cheby2(filtorder, dBrej, fpy, output = 'sos')
    filly2 = IIRFilter(cheb2) 
    
    #Calculation of frequency response of filter
    w_c2, h_c2 = signal.freqz(b_c2, a_c2)
    vertline = fc/fs #normalised value
    
    #Plot of frequency response of filter
    plt.close(1)
    plt.figure(1)
    plt.plot(w_c2/np.pi/2, 20*np.log10(np.abs(h_c2)))
    plt.axvline(1/fs, color="green") #Green line at 1Hz
    plt.axvline(vertline, color="red") #Red line at chosen cut-off frequency
    plt.title("Frequency characteristics of filter. Fs = "+str(fs)+"Hz. Fc = "+str(fc)+"Hz. Green line at 1Hz, red line at "+str(fc)+"Hz.") #title with red line frequency
    #plt.title("Frequency characteristics of filter. Fs = "+str(fs)+"Hz. Fc = "+str(fc)+"Hz. Green line at 1Hz") #title without red line frequency
    plt.xlabel("Normalised frequency")
    plt.ylabel("dB gain")
    
    #Test filtering
    duration = 20 #Wave duration
    t = np.linspace(0, duration, duration*fs, endpoint = False) #Creation of time axis
    #inputs = 10*np.sin(5*2*np.pi*t) + 2 #5Hz wave with amplitude 10 and DC offset of 2
    inputs = 10*np.sin(5*2*np.pi*t) + 2*np.sin(1*2*np.pi*t) + 2 #5Hz wave with amplitude 10, 1Hz wave with amplitude 2 and DC offset of 2
    outputs2 = []    
    for x in inputs:
        outputs2.append(filly2.filter(x))       
        
    #Plot of test filtering
    plt.close(2)
    plt.figure(2)
    plt.plot(t, inputs, color = "blue")
    plt.plot(t, outputs2, color = "red")
    plt.axhline(2, color = "lightblue")
    plt.title("Rejection test of 5Hz wave. Fs = "+str(fs)+"Hz. Fc = "+str(fc)+"Hz.")
    plt.xlabel("time(s)")
    plt.ylabel("Amplitude")
    
    plt.show()