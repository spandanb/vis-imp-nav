import SimpleCV as scv
import numpy as np
import sys
import socket
sys.path.append('./directions')
from clist import CList
from speak import speak
from phoneImu import PhoneIMU
#import userinput2 as uinp
from userinput2 import UserInput
from directions2 import Directions
from getch import _Getch

idxmap=["All", "Left", "Center", "Right", "Back"]
dirmap={"all":0, "left":1, "center":2, "right":3, "back":4}

class Walk():

    def __init__(self, n=5):
        self.cam = scv.Kinect()
        #initialize meanvect
        self.meanvect = CList(n)
        for i in range(n):
            self.meanvect.push(self.getavg())
        self.oldidx = -1 #old
                    
    def getavg(self):
        dm=self.cam.getDepthMatrix()
        #Get depth and height
        h,w = dm.shape #h=480, w=640
        
        left  = dm[:, 0:w/2]
        center = dm[:, w/4:3*w/4]
        right = dm[:, w/2:]
        
        leftMean = np.sum(left)/left.size
        centerMean = np.sum(center)/center.size
        rightMean = np.sum(right)/right.size
        mean = np.sum(dm)/dm.size
        return np.array([mean, leftMean, centerMean, rightMean])
    
    def walk(self,n=5):                
        
        newidx =  -1
        smat = self.meanvect.getn(n=n) #sample matrix
        median = np.median(smat, axis=0)        
        minidx = median.argmin()
        
        #backup if against a wall
        if median[dirmap["all"]] > 1900:            
            newidx=dirmap["back"]
                
        #walk in center if walkable
        elif median[dirmap["center"]] <= 1100 or minidx == dirmap["center"]:           
            newidx = dirmap["center"]
        
        else: #pick left or right based on whichever is cleaner
            newidx = minidx
    
        #store new sample
        mean=self.getavg()
        self.meanvect.push(mean)
        
        #print "{} {}".format(newidx, self.oldidx)             
        if newidx != self.oldidx:
            self.oldidx=newidx
            return newidx
        else:    
            return -1

def getIPAddr():
    return socket.gethostbyname(socket.getfqdn()) 


if __name__ == '__main__':
    
    #sys.argv
    
    wEn = False #walk
    iEn = True #imu
    uEn = True #user input
    dEn = True #directions
    getch = _Getch()
    spoken = False
    if wEn:
        walk = Walk()
    
    if iEn:
        print getIPAddr()
        ipaddr = getIPAddr() #of this machine
        port = 5001
        imu = PhoneIMU(ipaddr, port)
        olddirc = None #direction reading
        newdirc = None
    
    if uEn:
        ch = [None]
        #uin = UserInput(ch)
        #uin.start()
        oldch = None #user input
        newch = None

    if dEn:
        start = "40 St George St, Toronto, ON, M5S2E4"
        end = "220 Yonge St, Toronto, ON M5B2H1" 
        directions = Directions(start, end)
        steps = directions.getsteps()
    
    print "Entering main loop"
    while True:                     
        """
        newdirc = imu.getdirc() #get direction        
        if newdirc != olddirc:
            print "Dir is {}".format(newdirc)
            olddirc = newdirc
        """
        print "Reading variable"
        newch = getch() 
        print "newch is {}".format(newch)
        #if not spoken: #newch != oldch:
        print "char is {}".format(newch)  
        oldch = newch                
        text = None
        
        
        try:
            #speak based on input
            if newch == "s": #start location
                text = "Start location is {}".format(start) 
            elif newch == "e": #end location
                text = "End location is {}".format(end)
            elif newch == "d": #direction (compass heading)
                text = "You are facing {}".format(olddirc)
            elif newch == "f": #next step
                text = steps[0]
            elif newch == "q" or ord(newch) == 27:
                sys.exit()
                #TODO: handle exit logic
            if text:
                #print text
                speak(text)
            print "text is '{}'".format(text)   
        except Exception as e:
            print e
            
        