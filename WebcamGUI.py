# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 21:10:46 2020

@author: ellaw
"""

import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import style
style.use("ggplot")
import numpy as np
import PIL.Image, PIL.ImageTk

LARGE_FONT = ("Verdana", 12)
  

class RealtimePlotWindow:
    def __init__(self):
        self.fig  = Figure(figsize=(7,6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel("Index value")
        self.ax.set_ylabel("Colour value")
        self.ax.set_title("RGB values")
        self.plotbufferr = np.zeros(500)
        self.plotbufferg = np.zeros(500)
        self.plotbufferb = np.zeros(500)
        self.liner, = self.ax.plot(self.plotbufferr, color="red", linewidth = 0.8)
        self.lineg, = self.ax.plot(self.plotbufferg, color = "green", linewidth = 0.8)
        self.lineb, = self.ax.plot(self.plotbufferb, color = "blue", linewidth = 0.8)
        self.ax.set_ylim(-1, 270)
        self.ringbufferr = []
        self.ringbufferg = []
        self.ringbufferb = []

        
    def update(self, data):
        self.plotbufferr = np.append(self.plotbufferr, self.ringbufferr)
        self.plotbufferr = self.plotbufferr[-500:]
        self.ringbufferr = []
        self.liner.set_ydata(self.plotbufferr)
        self.plotbufferg = np.append(self.plotbufferg, self.ringbufferg)
        self.plotbufferg = self.plotbufferg[-500:]
        self.ringbufferg = []
        self.lineg.set_ydata(self.plotbufferg)
        self.plotbufferb = np.append(self.plotbufferb, self.ringbufferb)
        self.plotbufferb = self.plotbufferb[-500:]
        self.ringbufferb = []
        self.lineb.set_ydata(self.plotbufferb)
        return self.liner, self.lineg, self.lineb,

    def addDatar(self, v):
        self.ringbufferr.append(v)

    def addDatag(self, v):
        self.ringbufferg.append(v)

    def addDatab(self, v):
        self.ringbufferb.append(v)

class CameraGUI(tk.Tk):
    '''Overall GUI containter class'''
    def __init__(self, camera, cammethod):
        tk.Tk.__init__(self)
        #tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self,default="clienticon.ico") #Doesnt work  with apple '''
        tk.Tk.wm_title(self, "WebCamera monitor")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=1)
        container.grid_rowconfigure(2, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_columnconfigure(2, weight=1)
        
        self.RTP = RealtimePlotWindow()
        self.cammethod = cammethod #method for starting camera class
        self.camera = camera #assigns camera class 
        self.cameraon = 0
        
        self.camerawidth = 640
        self.cameraheight = 480
        #self.flashcam() #
        
        #Dictionary creation
        self.frames = {} 
        for F in (CameraFeed,RGBPlot):
            if F == RGBPlot:
                frame = F(container, self)
            else:
                frame = F(container, self)
            self.frames[F] = frame        
            frame.grid(row=0, column=0, sticky="nsew") #pack or grid
            #frame.grid_rowconfigure(0, weight=1)
            #frame.grid_columnconfigure(0, weight=1)
        
        self.showFrame(RGBPlot) #Shows default page
    
    
    def flashcam(self):
        '''Cycles the users cam on, grabs dimensions and then turns the camera off again'''
        self.GUIcamstart()
        self.camerawidth, self.cameraheight = self.camera.getGeometry()
        self.GUIcamstop()
    
    
    def showFrame(self, control):
        '''Changes page'''
        frame = self.frames[control]
        frame.tkraise()
        
     
    def checkcam(self):
        '''Checks to see if camera is open. Returns a 1 if open.'''
        try:
            if self.camera.cam.isOpened():
                self.cameraon = 1
                return 1
            else:
                self.cameraon = 0
                return 0
        except:
            return 0
        

    def GUIcamstart(self):
        '''GUI method to start camera. Returns 1 if successful, otherwise a 0'''
        if not self.checkcam():
            try:
                self.camera.start(self.cammethod, cameraNumber = 0)
                self.cameraon = 1
                if self.checkcam():
                    print("Camera started")
                    return 1
                else:
                    print("Camera failed to open")
            except:
                print("Webcam2rgb start method failed.")
        else:
            print("Camera already on")
        return 0
            
            
    def GUIcamstop(self):
        '''GUI method to stop camera. Returns 1 if successful, otherwise a 0'''
        if self.checkcam():
            try:
                self.camera.stop()
                self.cameraon = 0
                print("Stopping camera")
                return 1
            except:
                print("Webcam2rgb stop method failed")
        else:
            print("Camera not on")
        return 0
        
        
        
class RGBPlot(tk.Frame):
    '''RGB plotting page'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="RGB Plot", font=LARGE_FONT)        
        label.grid(row=0, column = 0, padx=10,pady=10)
        
        button = tk.Button(self, text="Go to camera feed",width = 30,
                            command=lambda: controller.showFrame(CameraFeed))
        button.grid(row=0, column=1,padx=10, pady=10)
        
        self.toggleFeedbutton = tk.Button(self, text="Enable camera feed",width = 30, bg="#70db70",
                            command=lambda: self.toggleFeed(controller))
        self.toggleFeedbutton.grid(row=0, column=2, padx=10, pady=10)

        
        canvas = FigureCanvasTkAgg(controller.RTP.fig, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, columnspan=3)        
        
        toolbarFrame = tk.Frame(self)
        toolbarFrame.grid(row=2, columnspan=3)
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
        toolbar.update()
        
        
    def toggleFeed(self, controller):
        '''Method for Enable/Disable camera feed button'''
        if self.toggleFeedbutton.config("text")[-1] == "Enable camera feed":
            if controller.GUIcamstart():
                self.toggleFeedbutton.config(text="Disable camera feed",bg="#ff4d4d")
        else:
            if controller.GUIcamstop():
                self.toggleFeedbutton.config(text="Enable camera feed", bg="#70db70")
        

class CameraFeed(tk.Frame):
    '''Web camera feed page'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Camera feed", font=LARGE_FONT)        
        label.grid(row=0, column=0,padx=10, pady=10)
        
        button = tk.Button(self, text="Go to RGB Plot",width = 30,
                            command=lambda: controller.showFrame(RGBPlot))
        button.grid(row=0, column=1,padx=10, pady=10)
        
        self.stopvid = 1       
        self.toggleShowbutton = tk.Button(self, text="Show me",width = 30, bg="#70db70",
                            command=lambda: self.toggleShow(controller))
        self.toggleShowbutton.grid(row=0, column=2, padx=10, pady=10)
        
        self.cameradelay = 33  

        self.canvasoffsetw = controller.camerawidth/2
        self.canvasoffseth = controller.cameraheight/2
        
        self.canvas = tk.Canvas(self, width = controller.camerawidth, height = controller.cameraheight)#place in webcam page
        self.canvas.grid(row=2, columnspan=3, padx=10, pady=10)
        
        self.imgnoten =  PIL.ImageTk.PhotoImage(PIL.Image.open("NotEnabledImg.png"))
        self.imgnoshow =  PIL.ImageTk.PhotoImage(PIL.Image.open("NoShowImg.png"))
        self.canvas.create_image(self.canvasoffsetw, self.canvasoffseth, image = self.imgnoshow)
        
    
    def toggleShow(self, controller):
        if self.toggleShowbutton.config("text")[-1] == "Show me":
            if not self.cameraupdatestart(controller):
                self.canvas.create_image(self.canvasoffsetw, self.canvasoffseth, image = self.imgnoten)
            self.toggleShowbutton.config(text="Stop showing me",bg="#ff4d4d")
        else:
            self.cameraupdatestop(controller)
            self.toggleShowbutton.config(text="Show me", bg="#70db70")
      
        
    def cameraupdatestart(self, controller):
        self.stopvid = 0
        if not controller.checkcam(): #checks to see if camera is on
            return 0
        self.cameraupdate(controller)
        return 1
    
    
    def cameraupdatestop(self,controller):
        self.stopvid = 1
        try:
            controller.after_cancel(self.videofeed)
        except:
            self.stopvid = 1 #Repeated line to fill except clause
        finally:    
            #self.canvas.delete("all")
            self.canvas.create_image(self.canvasoffsetw, self.canvasoffseth, image = self.imgnoshow)
        
        
    def cameraupdate(self, controller):
        ret, frame = controller.camera.get_frame()
        
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(self.canvasoffsetw, self.canvasoffseth, image = self.photo) #Offsets needed, perhaps as canvas is smaller than photo, default sticky is center
            #self.canvas.create_image(self.canvasoffsetw, self.canvasoffseth, image = self.photo, sticky=tk.NW) #sticky doesnt work?
        
        if self.stopvid:
            return 0
        
        self.videofeed = controller.after(self.cameradelay, self.cameraupdate, controller)
