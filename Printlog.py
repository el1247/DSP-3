# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 23:34:51 2020

@author: ellaw
"""

import numpy as np
import matplotlib.pyplot as plt

fs = 17

#log = np.loadtxt("loglogLongpink.txt")
log = np.loadtxt("loglog1Pink.txt")
red = log[0]
green = log[1]
blue = log[2]
length = len(red)
duration = length/fs

t = np.linspace(0,duration, length, endpoint = False)

plt.figure(1)
plt.plot(t, red, color = "red")
plt.plot(t, green, color = "green")
plt.plot(t, blue, color = "blue")
plt.title("Raw data")
plt.xlabel("Time(s)")
plt.ylabel("RGB values")

fftred = np.fft.fft(red)
fftgreen = np.fft.fft(green)
fftblue = np.fft.fft(blue)


plt.figure(2)
faxis = np.linspace(0,fs,length,endpoint=False)
plt.plot(faxis, np.abs(fftred), color = "red")
plt.plot(faxis, np.abs(fftgreen), color = "green")
plt.plot(faxis, np.abs(fftblue), color = "blue")
plt.title("Raw data frequency spectrum")
plt.xlabel("Frequency(Hz)")
plt.ylabel("Amplitude")