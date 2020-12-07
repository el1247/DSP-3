
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 11:56:41 2020

@author: ellaw
"""
import webcam2rgb #Use this for direct show backend testing
import time
import numpy as np


class camerachecking():  
    def __init__(self):
        self.log = []
        
    def camtest(self,duration, method, iteration):
        print("--------------")
        #Variable and class initialization
        cams = webcam2rgb.Webcam2rgb()    #Creating an instance of the camera class
        
        #Camera start section
        cams.start(method, cameraNumber= 0, directShow = True) #directShow = True uses DSHOW backend, = False uses MSMF on windows 
        
        #Waiting for camera opening section
        while not cams.cam.isOpened():
            continue
        print("The cameras stated sample rate is "+str(cams.cameraFs())+"Hz.") #Placed before camera start statement for users sake if trying to self time.
        print("Camera started")
        
        #Initial wait
        start = time.time()
        expectedend = start + 1
        while time.time() < expectedend:
            continue

        #Start of test
        self.log = []
        start = time.time()
        expectedend = start + duration
        
        #Check for time elapsed
        while time.time() < expectedend:
            continue
        end = time.time()
        
        #Stopping camera section
        cams.stop
        cams.cam.release()
        print("Camera stopped")
        
        #Results section
        loglength = len(self.log)
        frequency = round(loglength/duration,2)
        print("Iteration "+str(iteration)+". Test duration = " +str(end-start))
        print("The captured number of frames in "+str(duration)+" seconds is "+str(loglength)+", which yields a sample rate of "+str(frequency)+"Hz.")       
        return loglength,frequency

    

def hasData(retval, data):
    '''Method to be passed to camera class for callback each frame'''
    r = data[2] #Identifies red value for frame
    camscheck.log.append(r) #Appends red value to the list


#Main section
camscheck = camerachecking()
overalllog = [[],[],[]]
count = int(input("Enter number of tests: "))
durationtype = 2
while not(durationtype == 1 or durationtype ==0): 
    durationtype = int(input("Fixed(0) or dynamic(1) test durations: "))
durationm = 10
for i in range(1,count+1):
    if durationtype:
        durationm = i #increments duration equal to iterater
    lengthm, frequencym = camscheck.camtest(durationm,hasData, i)
    overalllog[0].append(durationm)
    overalllog[1].append(lengthm)  
    overalllog[2].append(frequencym)  

#Printing of results
print("\n-----------------------------------")   
if durationtype:
    print(str(count)+" tests ran with a duration equal to the test number in seconds.")
else:
    print(str(count)+" tests ran with a duration of "+str(durationm)+" seconds each.") 
print("The samples had a maximum of "+str(np.max(overalllog[1]))+" and a minimum of "+str(np.min(overalllog[1])))
print("Average sampling frequency = "+str(np.average(overalllog[2]))+"Hz. With a maximum of "+str(np.max(overalllog[2]))+"Hz and a minimum of "+str(np.min(overalllog[2]))+"Hz.")
