import SimpleCV as scv
import numpy as np
import subprocess as sp
import time

last_call = time.time()

#Arg must be string
def speak(arg):
    global last_call
    if isinstance(arg, str):
        cmd =  ["say", arg ]
    elif isinstance(arg, list):
        cmd=["say"] + arg
    else:
        cmd = None
        print "Error: Unknown arg type"
    if cmd:
        if time.time() - last_call > 5:
            sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
            last_call = time.time()

#Get the normalized view by sampling initial view
def getNorm(cam, samples=2):
    leftNorm = 0
    rightNorm = 0
    for i in range(samples):
        dm = cam.getDepthMatrix()
        h,w = dm.shape #h=480, w=640    
        left  = dm[:, 0:w/2]
        right = dm[:, w/2:]
        leftNorm += np.sum(left)
        rightNorm += np.sum(right)
    leftNorm /= samples
    rightNorm/= samples
    return [leftNorm, rightNorm]

if __name__ == '__main__':

    cam = scv.Kinect()    
    leftNorm, rightNorm = getNorm(cam)
    #print "leftNorm is {}. rightNorm is {}".format(leftNorm, rightNorm)
    leftMem = [leftNorm] * 5 #Memory
    rightMem = [rightNorm] * 5 #Memory
    while True:
            depth = cam.getDepth()
            depth.show()
            
            dm=cam.getDepthMatrix()
            #Get depth and height
            h,w = dm.shape #h=480, w=640
            
            left  = dm[:, 0:w/2]
            center = dm[:, w/4:3*w/4]
            right = dm[:, w/2:]
            
            leftWeight = np.sum(left)
            centerWeight = np.sum(center)
            rightWeight = np.sum(right)
            """
            print leftWeight #/float(leftNorm)
            print centerWeight
            print rightWeight #/float(rightNorm)
            print " "
            """
            """
            if leftWeight > rightWeight:
                print "Left"
            else:
                print "Right"
            """    
            r =  centerWeight / float(rightWeight)
            l = centerWeight / float(leftWeight) 
            if r > 1.2 or r < 0.8:
                speak("Go right")
            elif l > 1.2 or l < 0.8:
                speak("Go left")
            else:
                pass #print "Straight"