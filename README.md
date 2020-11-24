# DSP-3
Digital Signal Processing Assignment 3

This is a user interface that shows the RGB values of the center pixel of a webcam in real time.

Media folder
-----------------
Contains all the media formats used by the GUI
-clienticon.ico    Icon used for the GUI. Does not currently work on MAC OS.
-clienticon.xbm    Icon used for the GUI on Mac OS. Does not currently work on Windows OS
-NoShowImg.png     Custom made graphic of dimensions 640x480 that says No Show on it.
-NotEnabledImg.png Custom made graphic of dimensions 640x480 that says Camera Not Enabled on it.

-------------------------------------

webcam2rgb.py
-----------------
Course provided class to open and use webcam.

-------------------------------------

webcam2rgbplus.py
-----------------
Class file containing a subclass of webcam2rgb.py with some redfined methods and other additional methods.

-------------------------------------

WebcamGUI.py
-----------------
Code for the user interface and plot. Uses the methods of the webcam2rgbplus class.

-------------------------------------

WebcamMain.py
-----------------
Main code that creates an instance of the webcam2rgbplus class, defines plotting data method for GUI and launches GUI.

-------------------------------------

iir_filter.py
-----------------
Class file containg IIR_filter class that is used to filter input RGB data and return filtered values
