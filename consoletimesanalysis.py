# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 13:06:13 2020

@author: ellaw
"""

import numpy as np
import matplotlib.pyplot as plt

times = np.loadtxt("consoletimes.dat")
starts = times[0]

cleantimes = times - starts
newtimes = []
roundtimes = []

for i in range(15,len(cleantimes) - 1):
    x = cleantimes[i] - cleantimes[i-1]
    newtimes.append(x)
    roundtimes.append(round(x,4))

plt.close(1)
plt.figure(1)
plt.plot(newtimes, color = "blue")
plt.axhline(y=1/15, color = "red")
plt.title("Time since last call for camera in WebcamMain.py. Red line represents 15Hz time")
plt.xlabel("Index")
plt.ylabel("Time(s)")
plt.show()

averagenew = sum(newtimes)/len(newtimes)
print("The average difference in times between camera samples was "
      +str(round(averagenew,5))+" seconds. This gives a frequency of "+str(round(1/averagenew,3))+"Hz.")