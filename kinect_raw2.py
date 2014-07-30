import SimpleCV as scv
import numpy as np

class CList():
    def __repr__(self):
        #return self.vect
        oldest = (self.idx+1)%self.size
        return str(self.vect[oldest:] + self.vect[:oldest]) #oldest -> newest
    
    def __init__(self,size):
        self.vect = [None]*size
        self.idx = 0 #where newest element is
        self.size = size 
    
    #Put element in list 
    def push(self, arg):
        self.idx = (self.idx + 1) % self.size
        self.vect[self.idx] = arg        
    
    #Get last element 
    def get(self):
        return self.vect[self.idx] 
    
    #get lastN elements
    def getn(self, n=0, last=False):
        oldest = (self.idx+1)%self.size #oldest index
        if last: #only return first and last index
            return [self.vect[oldest], self.vect[self.idx]]
        
        if n<=0 or n>self.size:
            raise Exception
        
        if n == self.size:            
            return self.vect[oldest:] + self.vect[:oldest]
 
        head = self.vect[:self.idx+1]
        if len(head) >= n:
            firstidx = len(head) - n
            return head[firstidx:]        
        else:
            tail = self.vect[self.idx+1:]
            firstidx = len(tail) - (n-len(head))#first index of tail
            return tail[firstidx:] + head
          
    def raw(self):
        return self.vect
    
    
cam = scv.Kinect()
idxmap=["All", "Left", "Center", "Right", "Back"]
dirmap={"all":0, "left":1, "center":2, "right":3, "back":4}

def show():
    depth = cam.getDepth()
    depth.show()
    return depth
    
"""
Does average using 11 bit matrix 
"""
def getavg():
    #depth = cam.getDepth().getNumpy() #8-bit depth matrix
    
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

"""
@ret: returns max index of avg, i.e.
    where max value occurs
"""
def getmax(avg):    
    return avg.argmax()


"""
prints max 
"""
def getmax2():
    oldidx = -1
    while True:
        #depth = cam.getDepth()
        #depth.show()
        
        mean = getavg()        
        #where max is located
        maxidx = mean.argmax()      
        if maxidx != oldidx:
            print idxmap[maxidx]
            print mean
            oldidx=maxidx



"""
Over n periods, who where has the highest change occured 
"""
def getdiff():    
    n=5
    
    #initialize
    meanvect = CList(n)
    for i in range(n):
        meanvect.push(getavg())
    
    oldidx = -1
    while True:        
        #n captures gap between frames
        mean =  meanvect.getn(n=5)
        diff = np.fabs(mean[4] - mean[0])
        maxidx = diff.argmax() #index where max difference occurs
        if maxidx != oldidx and diff.max() > 100 and maxidx%2 == 1: #idx should be left or right
            print "{} diff={} new={} old={}".format(idxmap[maxidx], diff, mean[4], mean[0])
            oldidx=maxidx
        meanvect.push(getavg())    
            
    #in general, diff between 2 frames, n samples apart 
    diff = diffvect[-1] - diffvect[0] #newest - oldest
    maxidx = diff.argmax()
    
    #
    step = 1
    
def getmax3():
    oldidx = -1
    while True:
        #depth = cam.getDepth()
        #depth.show()
        
        mean = getavg()        
        #where max is located
        maxidx = mean.argmax()      
        if maxidx != oldidx:
            print idxmap[maxidx]
            print mean
            oldidx=maxidx    
    

#combines logic behind getmax2 and getdiff
def walk():
    n=5
    
    #initialize
    meanvect = CList(n)
    for i in range(n):
        meanvect.push(getavg())
    
    oldidx = -1
    newidx = -1 
    while True:        
        smat = meanvect.getn(n=n) #sample matrix
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
                         
        if newidx != oldidx:
            print idxmap[newidx]
            #print mean
            oldidx=newidx
            
        #store new sample    
        mean=getavg()
        meanvect.push(mean)
        
        

def diff2():   
    mlen = 5
    midx = 0
    mem = [avg2() for i in range(mlen)] #Initialize
    oldidx = -1 
    
    while True:
        mem[midx] = avg2() #Store value
        delta = mem[midx] - mem[(midx-1)%mlen] #get diff between newest and next-to-newest
        deltaAbs = np.fabs(delta) 
        
        maxidx = deltaAbs.argmax() #idx where distance has changed the most
        
        if deltaAbs[maxidx] > 100 and oldidx != maxidx:
            print "{}".format(idxmap[maxidx])
            oldidx = maxidx
            
            
        midx = (midx+1)%mlen #increment midx
        
if __name__ == '__main__':
    #getdiff()
    #getmax2()
    walk()
    while True:
        depth = cam.getDepth()
        depth.show()
        print getavg()
    
    """
    mlen = 2 #size of "memory"
    mem = [None]*mlen
    mptr = 0
    incr = lambda mptr: (mptr + 1) % mlen 
        
    oldidx = -1
    while True:
        #depth = cam.getDepth()
        #depth.show()
        
        mean = getavg()        
        #where max is located
        maxidx = mean.argmax()      
        if maxidx != oldidx:
            print idxmap[maxidx]
            oldidx=maxidx
    """    
        