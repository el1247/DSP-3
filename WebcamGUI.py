# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 21:10:46 2020

@author: ellaw
"""

import tkinter as tk
#from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
#import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib import style
style.use("ggplot")
import numpy as np
import PIL.Image, PIL.ImageTk
import os


LARGE_FONT = ("Verdana", 12) #Constant created for font consistancy
  

'''Idea log: Change try/except in init of CameraGUI for logo into OS specific code. May need to import platform: https://stackoverflow.com/questions/1854/python-what-os-am-i-running-on#:~:text=If%20you%20want%20to%20check,OS%20itself%20then%20use%20sys.
Issue with enabling show me, switching to RGB plot, enabling camera and then switching back to camera view
Redundant variables: self.cameraon currently is never used, leave for now

'''


class RealtimePlotWindow:
    '''Class used to animate a plot. A created instance has 3 memory channels: r g and b stored in associated index positions. Channels are updated
    using the addData method. Call the update function to move the data into the graph memory. Call update when animating.'''
    def __init__(self, samplerate = 1):
        '''Initialiser. Creates 3 numpy arrays of size 500 containing all 0s'''
        self.fig  = Figure(figsize=(7,6), dpi=100) #Creates instance of figure. Adjust size here
        self.ax = self.fig.add_subplot(111)
        self.plotbuffers = [np.zeros(500), np.zeros(500), np.zeros(500)] #Creation of arrays
        
        if samplerate < 1:
            samplerate = 1
        self.xaxis = np.linspace(500/samplerate, 0, 500, endpoint = False) #Creates X axis to be used to scale graph #Running from high to low inverts data
                
        liner, = self.ax.plot(self.xaxis, self.plotbuffers[0], color="red", linewidth = 0.8)       #Creation of red line
        lineg, = self.ax.plot(self.xaxis, self.plotbuffers[1], color = "green", linewidth = 0.8)   #Creation of green line
        lineb, = self.ax.plot(self.xaxis, self.plotbuffers[2], color = "blue", linewidth = 0.8)    #Creation of blue line
        self.lines = [liner, lineg, lineb] #Creation of lines array

        if samplerate == 1:  
            self.ax.set_xlabel("Index value") #X axis label
        else:
            self.ax.set_xlabel("Time since measurement(s)") #X axis label
        self.ax.set_ylabel("Colour value") #Y axis label
        self.ax.set_title("RGB values") #Plot title
        self.ax.set_ylim(-1, 270) #Y axis limits
        self.ringbuffers = [[],[],[]] #Creation of ring buffers


    def update(self, data):
        '''Used to merge the ring buffer with the plot buffer. Needs to be called for animation'''
        for i in range(3):     #Loop 3 times for the r, g and b channels
            self.plotbuffers[i] = np.append(self.plotbuffers[i], self.ringbuffers[i]) #Adds the values in ringbuffer to the end of the plotbuffer array
            self.plotbuffers[i] = self.plotbuffers[i][-500:] #Takes last 500 values in plotbuffer and removes the rest
            self.ringbuffers[i] = [] #Empties the ring buffer
            self.lines[i].set_ydata(self.plotbuffers[i]) #Redraws the line with the new plot buffer information
        return self.lines #Returns the lines to be drawn
    
    
    def addData(self, r=0, g=0, b=0):
        '''Method of inserting new data into the ring buffer. Add data here, in the (r, g, b) order. Missing values will be set to 0'''
        self.ringbuffers[0].append(r)
        self.ringbuffers[1].append(g)
        self.ringbuffers[2].append(b)



class CameraGUI(tk.Tk):
    '''Overall GUI containter class. Creates and stores 1 instance of each of the frame classes'''
    def __init__(self, camera, cammethod, *args, **kwargs):
        '''Initialiser'''
        tk.Tk.__init__(self, *args, **kwargs) #Tkinter initialiser
        
        self.os = os.name #Gets system OS name
        if self.os =="nt": #Check to see if os is windows
                self.directShow = True #Windows code
        else:
            self.directShow = False #Linux and MacOS code
        
        basepath = os.getcwd() #Gets current working directory
        self.mediapath = os.path.join(basepath, "media") #Creates path to the media folder inside working directory
        image = os.path.join(self.mediapath, "clienticon.ico") #Creates path to icon file for window
        
        #Try catch to add an icon to the window. If this fails this is purely an asthetic issue and is of no importance to functionality. Hence use of try/except is allowed
        try: #Attempting to add icon to window
            tk.Tk.iconbitmap(self,default=image) #Windows Icon
            self.icon = 1 #Indicates icon was a success
        except:
            try: #Attempting to add icon to window again using .xbm instead of .ico
                image = os.path.join(self.mediapath, "clienticon.xbm")  #Creates path to icon file for window
                self.call('wm','iconbitmap',self._w,tk.BitmapImage(file=image)) #Apple Icon
                self.icon = 1 #Indicates icon was a success
            except:
                self.icon = 0 #Indicates icon was a failure
        finally:
            
            tk.Tk.wm_title(self, "WebCamera monitor") #Sets window title
            
            container = tk.Frame(self) #Creates base frame to display different frames in
            container.pack(side="top", fill="both", expand=True)
            container.grid_rowconfigure(0, weight=1) #row configurations. 3 rows to expand equally
            container.grid_rowconfigure(1, weight=1)
            container.grid_rowconfigure(2, weight=1)
            container.grid_columnconfigure(0, weight=1) #column configurations. 3 columns to expand equally
            container.grid_columnconfigure(1, weight=1)
            container.grid_columnconfigure(2, weight=1)
            
            self.cammethod = cammethod #method for starting camera class
            self.camera = camera #assigns camera class 
            self.cameraon = 0 #Internal variable tracking if the camera is on
            
            self.camerawidth = 640 #Assumed camera width
            self.cameraheight = 480 #Assumed camera height
            self.camerafps = 30 #Assumed camera fps
            
            self.grabcamstat() #Method to aquire camera width, height and fps #seems to crash python on MacOS when uncommented
            
            self.RTPraw = RealtimePlotWindow(self.camerafps) #Creates instance of animated plot class to display the raw camera data
            self.RTPfilt = RealtimePlotWindow(self.camerafps)#Creates instance of animated plot class to display the filtered camera data
            self.RTPfilt.ax.set_title("RGB Filtered") #Resets the title of the filtered plot
            
            self.frames = {} #Creates a dictionary of possible frames to show
            for F in (CameraFeed,RGBPlot): #Enter all frame class names that are to be created and used
                frame = F(container, self) #Creates instance of frame class
                self.frames[F] = frame     #Stored frame instance   
                frame.grid(row=0, column=0, sticky="nsew") #exports frame instance to window
            self.showFrame(RGBPlot) #Shows default page
    
    
    def grabcamstat(self):
        '''Turns users camera on, grabs dimensions and then turns the camera off again'''
        self.GUIcamstart() #Turns camera on
        self.camerawidth, self.cameraheight = self.camera.getGeometry() #Gets cameras dimensions
        self.camerawidth = int(self.camerawidth) #data type conversion to integer
        self.cameraheight = int(self.cameraheight) #data type conversion to integer
        
        camerafs = self.camera.cameraFs() #Gets cameras sampling rate
        if camerafs:
            self.camerafps = int(camerafs)
        else:
            print("Warning: Observed sample rate is 0.")
        self.GUIcamstop() #Turns camera off
        print("Dimensions = "+str(self.camerawidth)+" x "+str(self.cameraheight)+". Sampling rate = "+str(self.camerafps)+". (Measured = "+str(camerafs)+")")
    
    
    def showFrame(self, control):
        '''Changes frame being displayed on the window'''
        frame = self.frames[control] #selects desires frame
        frame.tkraise() #Displays desired frame
        
     
    def checkcam(self):
        '''Checks to see if camera is open. Returns a 1 if open.'''
        '''Created to handle instances when program checks cameras state when camera instance hasnt been created yet'''
        try: #Try to handle errors when camera.cam does not exist as camera has not been started yet
            if self.camera.cam.isOpened(): #Checks if camera is open
                self.cameraon = 1
                return 1
            else:
                self.cameraon = 0
                return 0
        except:
            return 0
        

    def GUIcamstart(self):
        '''GUI method to start camera. Returns 1 if camera successfully opens, otherwise a 0 is returned'''
        if not self.checkcam(): #Checks camera is off
            try: #Attempts to start camera                                                 
                self.camera.start(self.cammethod, cameraNumber = 0, directShow = self.directShow) #Calls camera start method
                self.cameraon = 1
                if self.checkcam(): #Checks camera has successfully been turned on
                    print("Camera started")
                    return 1 #Returns 1 if camera successfully turned on
                else:
                    print("Camera failed to open")
            except:
                print("Webcam2rgb start method failed.")
        else:
            print("Camera already on")
        return 0 #Returns 0 if camera was already open or failed to open
            
            
    def GUIcamstop(self):
        '''GUI method to stop camera. Returns 1 if camera successfully stops, otherwise a 0 is returned'''
        if self.checkcam(): #Checks camera is on
            try:
                self.camera.stop() #Calls camera stop method
                self.cameraon = 0
                print("Stopping camera")
                return 1 #Returns 1 if camera successfully turns off
            except:
                print("Webcam2rgb stop method failed")
        else:
            print("Camera not on")
        return 0 #Returns 0 if camera is not open or failed to close
        
        
        
class RGBPlot(tk.Frame):
    '''RGB plotting page'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) #Calls tkinter initialiser
        self.colourdelay = 33
        
        #Top left label displaying page name
        label = tk.Label(self, text="RGB Plot", font=LARGE_FONT)        
        label.grid(row=0, column = 0, padx=10,pady=10)
        
        #Switch page button to CameraFeed page
        button = tk.Button(self, text="Go to camera feed",width = 30,
                            command=lambda: controller.showFrame(CameraFeed))
        button.grid(row=0, column=1,padx=10, pady=10)
        
        #Camera enable/disable button
        self.toggleFeedbutton = tk.Button(self, text="Enable camera feed",width = 30, bg="#70db70",
                            command=lambda: self.toggleFeed(controller))
        self.toggleFeedbutton.grid(row=0, column=2, padx=10, pady=10)

        #Top right label displaying colour
        self.labelc = tk.Label(self, text="#000000", font=LARGE_FONT)        
        self.labelc.grid(row=0, column = 3, padx=10,pady=10)

        #Left animated plot (animation function needs to be called in main code)
        canvas = FigureCanvasTkAgg(controller.RTPraw.fig, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, columnspan=3)        
        
        #Left plot tool bar
        toolbarFrame = tk.Frame(self)
        toolbarFrame.grid(row=2, columnspan=3)
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
        toolbar.update()
    
        #Right animated plot (animation function needs to be called in main code)
        canvas2 = FigureCanvasTkAgg(controller.RTPfilt.fig, self)
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=1, column=3, columnspan=3)
        
        #Right plot toolbar
        toolbarFrame = tk.Frame(self)
        toolbarFrame.grid(row=2, column=3, columnspan=3)
        toolbar = NavigationToolbar2Tk(canvas2, toolbarFrame)
        toolbar.update()
        
        
    def toggleFeed(self, controller):
        '''Method for Enable/Disable camera feed button'''
        if self.toggleFeedbutton.config("text")[-1] == "Enable camera feed": #Checks buttons current state
            if controller.GUIcamstart(): #Tries to call GUI camera start method. Condition passes if camera successfully opens
                self.toggleFeedbutton.config(text="Disable camera feed",bg="#ff4d4d") #Changes button display to disable option
                self.colourdisplay(controller)
        else:
            if controller.GUIcamstop(): #Tries to call GUI camera stop method. Condition passes if camera successfully closes
                self.toggleFeedbutton.config(text="Enable camera feed", bg="#70db70") #Changes button display to enable option
                self.after_cancel(self.colouris)
                
                
    def colourdisplay(self, controller):
        red = round(controller.RTPfilt.plotbuffers[0][499])
        green = round(controller.RTPfilt.plotbuffers[1][499])
        blue = round(controller.RTPfilt.plotbuffers[2][499])
        redh = hex(red)
        greenh = (hex(green))[2:]
        blueh = (hex(blue))[2:]
        value = redh + greenh + blueh
        self.labelc.config(text=value) 
        self.labelc.config(bg = ("#"+value[2:]))
        self.colouris = controller.after(self.colourdelay, self.colourdisplay, controller) #Method calls itself with a delay of self.cameradelay ms.
        
    def __del__(self):
        self.after_cancel(self.colouris)
        self.after_cancel(self.videofeed)


class CameraFeed(tk.Frame):
    '''Web camera feed page'''
    def __init__(self, parent, controller):
        '''Initialiser'''
        tk.Frame.__init__(self, parent)#Calls tkinter initialiser
        self.stopvid = 1
        
        #Top left label displaying page name
        label = tk.Label(self, text="Camera feed", font=LARGE_FONT)        
        label.grid(row=0, column=0,padx=10, pady=10)
        
        #Switch page button to RGBPlot page
        button = tk.Button(self, text="Go to RGB Plot",width = 30,
                            command=lambda: controller.showFrame(RGBPlot))
        button.grid(row=0, column=1,padx=10, pady=10)
        
        #Toggle button for show me/hide me
        self.toggleShowbutton = tk.Button(self, text="Show me",width = 30, bg="#70db70",
                            command=lambda: self.toggleShow(controller))
        self.toggleShowbutton.grid(row=0, column=2, padx=10, pady=10)
        
        self.cameradelay = 33  #Controls canvas refresh rate in ms. Set to 33 to give an approximate 30FPS refresh rate
        self.canvasoffsetw = controller.camerawidth/2  #Offset for camera screenshot in canvas, width. Set to midpoint based on captured camera dimensions
        self.canvasoffseth = controller.cameraheight/2 #Offset for camera screenshot in canvas, height. Set to midpoint based on captured camera dimensions
        
        #Canvas to display the webcam frames
        self.canvas = tk.Canvas(self, width = controller.camerawidth, height = controller.cameraheight)
        self.canvas.grid(row=2, columnspan=3, padx=10, pady=10)
        
        self.noimagenoten = 0 #Indicator to identify if camera not enabled image is successfully imported
        self.noimageshow = 0 #Indicator to identify if no show image is successfully imported
        try: #Attempt to import camera not enabled image
            image = os.path.join(controller.mediapath, "NotEnabledImg.png") #Combines media folder file path from CameraGUI to desired image
            self.imgnoten =  PIL.ImageTk.PhotoImage(PIL.Image.open(image)) #Imports image and stores in self.imgnoten
        except:
            self.noimagenoten = 1 #Indicator that there was an import error
        finally:
            try: #Attempt to import no show image
                image = os.path.join(controller.mediapath, "NoShowImg.png") #Combines media folder file path from CameraGUI to desired image
                self.imgnoshow =  PIL.ImageTk.PhotoImage(PIL.Image.open(image)) #Imports image and stores in self.imgnoshow
                self.canvas.create_image(self.canvasoffsetw, self.canvasoffseth, image = self.imgnoshow) #Draws no show image to canvas
            except:
                self.noimageshow = 1 #Indicator that there was an import error
        
    
    def toggleShow(self, controller):
        '''Method for show me/stop showing me button'''
        if self.toggleShowbutton.config("text")[-1] == "Show me": #Checks buttons current state. Show me state passes condition
            if not self.cameraupdatestart(controller): #Calls the start method for the image capture method. If start method is successful condition passes
                if not self.noimagenoten: #Checks if image is there to draw
                    self.canvas.create_image(self.canvasoffsetw, self.canvasoffseth, image = self.imgnoten) #Sends camera not enabled image to canvas
            self.toggleShowbutton.config(text="Stop showing me",bg="#ff4d4d") #Changes button state to stop showing me
        else:
            self.cameraupdatestop(controller) #Calls the stop method for the image capture method. 
            self.toggleShowbutton.config(text="Show me", bg="#70db70") #Changes button state to show me
      
        
    def cameraupdatestart(self, controller):
        '''Checks if camera is on. If it is starts the image capture method to redraw canvas'''
        self.stopvid = 0 #Used to stop cameraupdate method calling itself. 0 enables method to call itself
        if not controller.checkcam(): #checks to see if camera is on
            return 0 #returns 0 if camera is off
        self.cameraupdate(controller) #Calls method to display what the webcam is seeing
        return 1 #returns 1 to indicate method was successful
    
    
    def cameraupdatestop(self,controller):
        self.stopvid = 1 #Used to stop cameraupdate method calling itself. 1 stops this
        try:
            controller.after_cancel(self.videofeed) #Stops future callbacks of cameraupdate method. Try except in case there is no callback instance
        except:
            self.stopvid = 1 #Repeated line to fill except clause
        finally:    
            self.canvas.delete("all") #Clears canvas. Done for general cleanliness as well as the potential of webcam image being bigger than new image to be displayed 
            if not self.noimageshow: #Checks if image is there to draw
                self.canvas.create_image(self.canvasoffsetw, self.canvasoffseth, image = self.imgnoshow) #Sends no show image to canvas

        
    def cameraupdate(self, controller):
        '''Takes current camera frame and displays it on the frames canvas. Calls itself with a delay based on self.cameradelay'''
        ret, frame = controller.camera.get_frame() #Grabs current camera frame
        
        if ret: #If there is a frame
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame)) #Converts frame to photo
            self.canvas.create_image(self.canvasoffsetw, self.canvasoffseth, image = self.photo) #Displays photo on canvas #Offsets needed, perhaps as canvas is smaller than photo, default sticky is center
            #self.canvas.create_image(self.canvasoffsetw, self.canvasoffseth, image = self.photo, sticky=tk.NW) #sticky doesnt work?
        
        if self.stopvid: #Check to see if method should stop calling itself
            return 0 #Return to prevent method from calling itself
        
        self.videofeed = controller.after(self.cameradelay, self.cameraupdate, controller) #Method calls itself with a delay of self.cameradelay ms.
