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
        
        #Form 1 buffers
        self.bufferb1 = 0
        self.bufferb2 = 0
        self.buffera1 = 0
        self.buffera2 = 0
        

    def filter(self, x):
        '''Filter function. Takes in scalar x and returns scalar y'''
        '''1 accumulator 4 delays. Good for 2s complement addition and fixed point.'''
        adder = x*self.b0 + self.bufferb1*self.b1 + self.bufferb2*self.b2 - self.buffera1*self.a1 - self.buffera2*self.a2
        self.bufferb2 = self.bufferb1
        self.bufferb1 = x
        self.buffera2 = self.buffera1
        self.buffera1 = adder
        return adder



class IIRFilter():
    '''Chain of second order filters created by IIR2Filter'''
    def __init__(self, sosarray):
        self.IIR2Farray = []
        self.order = int(len(sosarray))
        for i in range(self.order):
            self.IIR2Farray.append(IIR2Filter(sosarray[i]))


    def filter(self, x):
        '''Filter function for class. Takes in a scalar x and returns scalar y, which has been filtered through all arrays in self.IIR2Farray'''
        y = x
        for i in self.IIR2Farray:
            y = i.filter(y)
            
        #Imposed limit specific to colour testing. Not implemented inside the loop or stored to prevent incorrect filtering of subsequent values
        if y > 255: #Max value for a single colour
            #print("Y exceeded colour max with a value of " + str(y))    
            y = 255 #Set returned value to max value for colour
            
        return y



#Start of main
if __name__ == '__main__':
    r = 0.9
    fc = 5
    fs = 30
    
    f = fc/fs
    fpy = f*2
    w0 = 2*np.pi*f  
    
    filtorder = 7
    
    b_b, a_b = signal.butter(filtorder, fpy)
    butts = signal.butter(filtorder,fpy, output = 'sos')
    
    b_c2, a_c2 = signal.cheby2(filtorder, 50, fpy)
    cheb2 = signal.cheby2(filtorder, 50, fpy, output = 'sos')
    
    filly1 = IIRFilter(butts) 
    filly2 = IIRFilter(cheb2) 
    
    duration = 100
    t = np.linspace(0, duration, duration*fs, endpoint = False)
    inputs = 10*np.sin(5*2*np.pi*t) + 2 #5Hz wave with amplitude 10 and DC offset of 2
    outputs1 = []
    outputs2 = []    
    for x in inputs:
        outputs1.append(filly1.filter(x))
        outputs2.append(filly2.filter(x))
        
    
    plt.figure(1)
    plt.plot(t, inputs, color = "blue")
    plt.plot(t, outputs1, color = "limegreen")
    plt.plot(t, outputs2, color = "orange")
    plt.axhline(2, color = "lightblue")
    
    
    print("SS error 1 = "+str(max(outputs1[-500:]) - 2))
    print("SS error 2 = "+str(max(outputs2[-500:]) - 2))
    
    
    w_b, h_b = signal.freqz(b_b, a_b)
    w_c2, h_c2 = signal.freqz(b_c2, a_c2)
    plt.figure(2)
    plt.plot(w_b/np.pi/2, 20*np.log10(np.abs(h_b)))
    plt.plot(w_c2/np.pi/2, 20*np.log10(np.abs(h_c2)))
    plt.axvline(5/fs)