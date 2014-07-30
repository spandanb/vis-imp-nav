import SimpleCV as scv
import numpy as np

cam = scv.Kinect()
idxmap=["All", "Left", "Center", "Right"]

def avg(depth=None):
    if not depth:
        depth = cam.getDepth()    
    mat = depth.getNumpy()
    mean = np.sum(mat)/mat.size
    return mean

def show():
    depth = cam.getDepth()
    depth.show()
    return depth
    
#avg(show())

"""
Does average using 11 bit matrix 
"""
def avg2():
    dm=cam.getDepthMatrix()
    #Get depth and height
    h,w = dm.shape #h=480, w=640
    
    left  = dm[:, 0:w/2]
    center = dm[:, w/4:3*w/4]
    right = dm[:, w/2:]
    
    leftMean = np.sum(left)/left.size
    centerMean = np.sum(center)/center.size
    rightMean = np.sum(right)/right.size
    mean = np.sum(dm)/dm.size
    #return (mean, leftMean, centerMean, rightMean)
    return np.array([mean, leftMean, centerMean, rightMean])

def getmax():
    
    oldval = None
    val = None
    while True:
        val = idxmap[avg2().argmax()]
        if oldval != val:
            print val
            oldval = val

"""
import kinect_raw as kr
kr.getmax2()
"""

def getmax2():
    mlen = 5
    mptr = 0
    mem = [avg2() for i in range(mlen)]

    maxArray = [] 
    
    oldidx = None
    idx = None
    while True:
        mem[mptr] = avg2()
        print mem
        maxArray = map(lambda arr: arr.argmax(), mem) #contains index of max element
        return maxArray
        bins = np.bincount(maxArray)
        print idxmap[bins.argmax()]
        """
        if oldval != val:
            print val
            oldval = val
        """
        mptr = (mptr + 1)%mlen

    
def diff():
    
    mlen = 5
    midx = 0
    mem = [None]*mlen
    for i in range(mlen):
        mem[i] = avg2() #Initialize
    olddiff = mem[4] - mem[0]
    oldidx = olddiff.argmax()
    while True:
        mem[midx] = avg2()        
        newdiff = mem[midx] - mem[(midx + 1)%mlen] #newest - oldest
        newidx = newdiff.argmax() #where distance has increased the most
        
        if np.fabs(newdiff[newidx] - olddiff[oldidx]) > 30:
            print "{}: NEW:{} OLD:{}".format(idxmap[newidx], newdiff, olddiff)
            olddiff = newdiff
            oldidx = newidx
            
        midx = (midx+1)%mlen #increment midx
        
        
def diff2():
    idxmap=["All", "Left", "Center", "Right"]
    mlen = 5
    midx = 0
    mem = [avg2() for i in range(mlen)] #Initialize
    oldidx = -1 
    
    while True:
        mem[midx] = avg2() #Store value
        delta = mem[midx] - mem[(midx-1)%mlen] #get diff between newest and next-to-newest
        deltaAbs = np.fabs(delta) 
        
        maxidx = deltaAbs.argmax() #idx where distance has changed the most
        
        if deltaAbs[maxidx] > 30 and oldidx != maxidx:
            print "{}".format(idxmap[maxidx])
            oldidx = maxidx
            
            
        midx = (midx+1)%mlen #increment midx
        
        
        