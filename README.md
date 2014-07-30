#Introduction
This project is a system that provides navigation assistance to visually impaired 
individuals. It uses the phone as an IMU (Inertial Measurement Unit), and gets the readings
from the magetometer, the accelerometer, and the gyroscope. In addition, we also use the
phone to determine the user's exact location. We combine this with the google directions
API to get directions. 

This is coupled with the Microsoft Kinect depth measurement feature. Whereas the directions API
provides directions in a environment free way, the depth map allows us to determine how to 
navigate locally. These two are combined to accurately and robustly allow the user to navigate.

In addition, this project contains the initial work for a keyer, which is any system that can be 
used to input a value. We use the phone IMU to detect user movements. Specifically, we define 
four motions: clockwise rotate, counter-clockwise rotate, lift the head of the phone up, and 
lift the tail of the phone up. These four actions can be used to encode all the alphabets, digits,
and a few other special characters.

#Files

clist.py: Data structure for circular list

codemap.py: Encoding used for the musical instruments.

coordinates: Gets coordinates of user using gyroscope and magnetometer.

depth\_test.py: Displays depth map of field of view of Kinect. Useful for debugging.

directions2.py: Used to get directions from some start location to destination location.
    Uses google directions API to get directions.

getch.py: Uses getch to get user entered char without newline.

getch2.py: Alternative to getch

kinect\_cam1.py: Script that analyzes depth map to determine which direction to walk in.
    Useful for debugging.

kinect\_cam2.py: Script that tests the depth map functionality of the Kinect. Useful for debugging.

kinect\_cam3.py: Script that tests the depth map functionality of the Kinect. Useful for debugging.

kinect\_cam4.py: Script that tests the depth map functionality of the Kinect. Useful for debugging.

kinect\_raw1.py: Script that has functions that are useful for debugging the the depth 
    map functionality of the Kinect.

kinect\_raw2.py: Script that has functions that are useful for debugging the the depth 
    map functionality of the Kinect.

phoneImu.py: Module that handles getting the IMU data from the phone. This includes the
    magnetometer, the accelerometer, and the gyroscope readings and the signal processing
    on the raw values to produce usable results. 

tesseract.py: Uses tesseract OCR engine to recognize and say the said text.

userinput.py: Module that reads user input via a second thread.

userinput2.py: Alternative implementation of user input reading functionality

walk1.py: Module that combines the directions sub-system with the phone IMU sub-system 
    to create a system that  allows the user to walk.

walk2.py: Similar to walk1.

walk3.py: Allows user to specify current location and destination. User can also query location and 
    orientation.

walk4.py: Initial work to allow user to input location using a keyer, where the phone is used as the 
    sensor and the keyer.

#NOTE

The video.py and common.py file is copied from the opencv-2.4.8 
distribution (opencv-2.4.8./samples/python2/\*.py).

The getch functionality is copied from the getch module.

This project was implemented for OS X. Specifically, certain  functions like
    speak may not work on other platforms, since they make use of native functions.


