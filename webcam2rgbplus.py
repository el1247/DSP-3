# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 09:36:05 2020

@author: ellaw
"""

import webcam2rgb
import cv2

class webcam2rgbplus(webcam2rgb.Webcam2rgb):
    '''Subclass of imported webcam2rgb class'''
    '''Overwritting of imported methods'''
    def __init___(self):
        webcam2rgb.Webcam2rgb.__init__()
    
    
    def start(self, callback, cameraNumber=0, width = None, height = None, fps = None, directShow = False):
        #print("Starting webcam") #Method already says opening camera
        webcam2rgb.Webcam2rgb.start(self, callback, cameraNumber, width, height, fps, directShow)
        
    
    def stop(self):
        try:
            webcam2rgb.Webcam2rgb.stop()
        except:
            print("Could not execute webcam2rgb.stop")
        try:
            self.cam.release() #Potentially try catch for no instance of cam?
        except:
            print("") #Prints nothing to console, in case app is closed without instance of webcam
        
    '''Custom classes'''
    def __del__(self):
        try:
            if self.cam.isOpened():
                self.cam.release()
        except:
            print("No instance of camera to close")
            
            
    def getGeometry(self):
        '''Returns width and height'''
        return [self.cam.get(cv2.CAP_PROP_FRAME_WIDTH),self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)]
    
    
    def get_frame(self):
        '''Used to take screen grabs of camera to display camera feed'''
        ret = False
        if self.cam.isOpened():
            ret, frame = self.cam.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)