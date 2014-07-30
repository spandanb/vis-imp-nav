import SimpleCV as scv
import numpy as np
import sys
import socket
from clist import CList
from speak import speak
from phoneImu import PhoneIMU
#import userinput2 as uinp
from userinput2 import UserInput
from directions2 import Directions
from getch import _Getch
import datetime
import coordinates as coord

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

def nSecElapsed(lastcall, time=2):
    return (lastcall - datetime.datetime.now() ).seconds > time



if __name__ == '__main__':
    
    def out(x): print x
    #out = lambda x: speak(x)
    
    wEn = False #walk
    iEn = True #imu
    dEn = True  #directions
    
    ipaddr = getIPAddr() #of this machine
    if wEn:
        walk = Walk()
    
    if iEn:      
        port = 5555
        print "PhoneIMU listening on {}:{}".format(ipaddr, port)
        imu = PhoneIMU(ipaddr=ipaddr, port=port)
        olddirc = None #direction reading
        newdirc = None
    
    if dEn:
        port = 5557
        print "Coordinates listening on {}:{}".format(ipaddr, port)
        #start = "40 St George St, Toronto, ON, M5S2E4"
        end = "220 Yonge St, Toronto, ON M5B2H1" 
        coord = coord.Coordinates(ipaddr=ipaddr, port=port)
        """
        conf = "N"
        while conf == "N":
            out("Enter Destination\n")
            end = raw_input(">> ")
            out("You entered {}".format(end))
            out("Confirm by entering y or n")
            conf = raw_input("y/n\n").lower()
            newStep = ""
            oldStep = ""
        """
        start = coord.getCoord()            
        directions = Directions(start, end)
        steps = directions.getsteps()
        
    lastcall = datetime.datetime.now()

    while True:
        
        if iEn:        
            newdirc = imu.getdirc() #get direction
            if newdirc != olddirc:
                out("Dir is {}".format(newdirc))
                olddirc = newdirc
                newStep = directions.getsteps(start=coord.getCoord())[0]
                if newStep != oldStep:
                    out("newStep is {}".format(newStep))
                    oldStep = newStep                            
        if wEn:        
            ret = walk.walk() #get walkable side       
            if ret != -1:
                d = idxmap[ret]
                nav = None
                if d != "Center":
                    if nSecElapsed(lastcall):
                        nav = "Go {}".format(d)
                else:
                    nav = "Go center"
                if nav:
                    out(nav)
                    lastcall = datetime.datetime.now()
