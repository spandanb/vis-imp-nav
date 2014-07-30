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
from getch2 import Getch, fetch
import datetime
import coordinates as coord

idxmap=["All", "Left", "Center", "Right", "Back"]
dirmap={"all":0, "left":1, "center":2, "right":3, "back":4}

#Output function
#def out(x): print x
out = lambda x: speak(x)

def log(arg):
    return 0
    print arg
    
class Hist():
    def __init__(self, val=None):
        self.val = val
        
    #Updates value and if updated returns new values, else None
    def update(self, new):
        if new != self.val:
            self.val = new
            return new
        return None #if value not updated
    
    def __getitem__(self):
        return self.val

class Walk():
    def __init__(self, n=5):
        self.cam = scv.Kinect()
        #initialize meanvect
        self.meanvect = CList(n)
        for i in range(n):
            self.meanvect.push(self.getavg())
        self.oldidx = -1 #old
    
    def getcam(self):
        return self.cam
                    
    def getavg(self):
        dm=self.cam.getDepthMatrix()
        #Get depth and height
        h,w = dm.shape #h=480, w=640
        
        left  = dm[:, 0:w/3] #dm[:, 0:w/2]
        center = dm[:, w/3: 2*w/3]#dm[:, w/4:3*w/4]
        right = dm[:, 2*w/3:]#dm[:, w/2:]
        
        leftMean = np.sum(left)/left.size
        centerMean = np.sum(center)/center.size
        rightMean = np.sum(right)/right.size
        mean = np.sum(dm)/dm.size
        return np.array([mean, leftMean, centerMean, rightMean])
    
    #return index of side to walk on;  idxmap[index] equals direction to walk
    def walk(self,n=5):                
        
        newidx =  -1
        smat = self.meanvect.getn(n=n) #sample matrix
        median = np.median(smat, axis=0)
        #print "median is {}".format(median)
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

def readDest():
    conf = "N"
    while conf != "y":
        out("Enter Destination\n")
        end = raw_input(">> ")
        out("You entered: {}".format(end))
        out("Confirm by entering y or n")
        conf = raw_input("y/n\n").lower()
    return end

def walkloop():
    walk = Walk() #walking object
    cam = walk.getcam()
    lastcall = datetime.datetime.now()
    lastspoken = ""
    while True:
        depth = cam.getDepth()
        depth.invert().show()
        
        ret = walk.walk() #get walkable side       
        if ret != -1:
            d = idxmap[ret]
            print "d is {}".format(d)
            nav = None
            if d != "Center":
                delta = datetime.datetime.now() - lastcall 
                msec = delta.seconds * 1000 + delta.microseconds/1000.0 
                print "time diff is {} msec".format(msec)
                if msec > 500:
                    nav = "Go {}".format(d)
            else:
                nav = "Go center"
            if nav:
                if lastspoken != nav:
                    out(nav)
                    lastspoken = nav
                lastcall = datetime.datetime.now()

if __name__ == '__main__':
    
    if len(sys.argv) > 1 and sys.argv[1] == "w":
        walkloop()
    
    wEn = False #walk
    dEn = True #directions
    iEn = True #imu-requires app    
    cEn = True #coordinates-requires app
    
    #getch = Getch()
    lastcall = datetime.datetime.now() 
    userInput = Hist()
    ipaddr = getIPAddr()
    
    nextStep = Hist() #next step
    nextElbow = Hist() #(lat long) of next turning-point
    here = Hist()   #Current location (lat, long)
    
    if wEn:
        walk = Walk() #walking object
        cam = walk.getcam()
       
    #(1) Get destination
    #end = readDest()
    end = "220 Yonge St, Toronto, ON M5B2H1"
    
    #(2) Get start location, i.e. current location
    port = 5007
    print "Listening for coordinates app at {}:{}".format(ipaddr, port)
    coord = coord.Coordinates(ipaddr=ipaddr, port=port)    
    start = coord.getCoord()            
    #start = "40 St George St, Toronto, ON, M5S2E4"
    print "Start is {}".format(start)
    
    #(3) Get directions
    directions = Directions(start, end)
    steps = directions.getsteps()
    print "Steps to {} are {}".format(end, steps)

    #90 -> N
    #180-> E
    #270-> S
    #0 | 360-> W

    port = 5005
    print "Listening for phoneIMU app at {}:{}".format(ipaddr, port)    
    imu = PhoneIMU(ipaddr, port)
    dirc = Hist() #direction reading
    rotcount = 99    
    rotwait = 100
    rotcmd = ""
    text = ""
    print "Entering main loop"
    while True:
        
        if wEn:
            depth = cam.getDepth()
            depth.show()
    
        if dirc.update(imu.getdirc3()):
            log("Current user direction is {}".format(dirc.val))
        
        #Update direction
        dirc.update(imu.getdirc3())
        if nextStep.update(directions.getsteps(start=coord.getCoord())[0]):
            log("nextStep is {}".format(nextStep.val))
            
        allSteps = directions.getStepCoords()
        
        if len(allSteps) > 1 and nextElbow.update(allSteps[1]): #if path only has one step        
            log("nextElbow is {}".format(nextElbow.val))
        
        if here.update(coord.getCoord(frmt=True)):
            log("here is {}".format(here.val))
            dist, brng = coord.getDistBrng(here.val, nextElbow.val)        
            log("distance from here to next elbow is {}, bearings are {}".format(dist, brng))
        
        #Compare nextElbow with current bearing and rotate accordingly
        if brng > dirc.val:
            brngDiff = brng - dirc.val
            if brngDiff > 45:
                rotcmd="Rotate by {} degrees Counter Clockwise".format(brngDiff)
                if rotcount >= rotwait:                    
                    out(rotcmd)
                    rotcount = 0
                else:
                    rotcount +=1
            else:
                rotcmd = "Walk straight ahead"
        else:
            brngDiff = dirc.val - brng
            if brngDiff > 45:
                rotcmd="Rotate by {:10.2f} degrees Clockwise".format(brngDiff)
                if rotcount >= rotwait:
                    out(rotcmd)
                    rotcount = 0
                else:
                    rotcount +=1
            else:
                rotcmd = "Walk straight ahead"
        
        #User input
        ch = fetch() #getch()
        if ch:
            ch=ch[0]
            print "User entered {}".format(ch)
        
        if userInput.update(ch):
            try:
                #speak based on input
                if userInput.val == "c": #current coordinates
                    text = "Current latitude is {:10.4f} and longitude is {:10.4f}".format(here.val[0], here.val[1]) 
                elif userInput.val == "e": #end location
                    text = "End location is {}".format(end)
                elif userInput.val == "d": #direction (compass heading)
                    text = "You are facing {}".format(olddirc)
                elif userInput.val == "f": #next step
                    text = nextStep.val
                elif userInput.val == "r":
                    text = rotcmd
                elif userInput.val == "q": #exit
                    sys.exit(1)
                if text:
                    out(text)
                print "text is '{}'".format(text)   
            except Exception as e:
                print e
        
        if wEn:        
            ret = walk.walk() #get walkable side       
            if ret != -1:
                d = idxmap[ret]
                nav = None
                if d != "Center":
                    if (datetime.datetime.now() - lastcall).seconds >2:
                        nav = "Go {}".format(d)
                else:
                    nav = "Go center"
                if nav:
                    out(nav)
                    lastcall = datetime.datetime.now()
        
