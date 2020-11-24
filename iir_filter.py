# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 16:31:47 2020

@author: ellaw
"""

import numpy as np
import matplotlib.pyplot as plt

class IIR_filter():
    '''Second order IIR filter Type 2'''
    def __init__(self, r, w):
        '''Initialisation, creates filter with characteristics of frequency w'''
        b0  = 1
        b1 = -2*np.cos(w)
        b2 = 1
        a0 = 1
        a1 = -2*r*np.cos(w)
        a2 = r**2
        
        self.b = [b0, b1, b2]
        self.a = [a0, a1, a2]
        self.buffer = [0, 0]
        
        self.inputlog = [[],[],[]]
        self.outputlog = [[],[],[]]
        
    
    def filt(self, v):
        self.inputlog[0].append(v)
        input_acc = 0
        output_acc = 0
        
        #IIR accumulator
        input_acc = v - self.a[1]*self.buffer[0] - self.a[2]*self.buffer[1]
        #FIR accumulator
        output_acc = self.b[0]*input_acc + self.b[1]*self.buffer[0] + self.b[2]*self.buffer[1]
        
        #Delay section
        self.buffer[1] = self.buffer[0]
        self.buffer[0] = input_acc
        self.outputlog[0].append(output_acc)
        return output_acc
    
    
    def filt3(self, r_in, g_in, b_in):
        self.inputlog[0].append(r_in)
        self.inputlog[1].append(g_in)
        self.inputlog[2].append(b_in)
        
        r_out = r_in+60
        g_out = g_in+60
        b_out = b_in+60
                
        self.outputlog[0].append(r_out)
        self.outputlog[1].append(g_out)
        self.outputlog[2].append(b_out)
        
        return r_out, g_out, b_out
        

if __name__ == '__main__':
    r = 0.2
    f = 0
    w = 2*np.pi*f  
    
    classy = IIR_filter(r, w)
    
    x = np.ones(50)
    xfilt = []

    for i in range(len(x)):
        xfilt.append(classy.filt(x[i]))

    plt.close(1)    
    plt.figure(1)    
    plt.plot(x, color = "blue")
    plt.plot(xfilt, color = "limegreen")
    plt.axvline(x=3)