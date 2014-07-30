import SimpleCV as scv
import numpy as np




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
            right = dm[:, w/2:]
            
            leftWeight = np.sum(left)
            rightWeight = np.sum(right)
            
            print leftWeight/float(leftNorm)
            print rightWeight/float(rightNorm)
            """
            if leftWeight > rightWeight:
                print "Left"
            else:
                print "Right"
            """    
        