import socket
import numpy as np
from collections import Counter
import sys
from speak import speak
import datetime

def getIPAddr():
    return socket.gethostbyname(socket.getfqdn()) 

class PhoneIMU():
    def __init__(self, ipaddr=getIPAddr(), port=5555):
        self.UDP_IP = ipaddr
        self.UDP_PORT = port

        self.sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
        self.sock.bind((self.UDP_IP, self.UDP_PORT))

    def getdirc(self):
        n=5
        mem = [None]*n
        for i in range(n): #get mode of n samples
            try:
                data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
                vect = data.split(",")
                acc = vect[2:5]    #accelerometer
                gyr = vect[6:9]    #gyroscope
                mag = vect[10:14]  #magnetometer readings
                
                #Use hx (i.e. mag[0]) and hy (i.e. mag[1])
                # to get dir as degrees 
                hx = float(mag[0])
                hy = float(mag[1])
                dirc = None
                #https://www.google.ca/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0CCsQFjAA&url=http%3A%2F%2Faerospace.honeywell.com%2F~%2Fmedia%2FUWSAero%2Fcommon%2Fdocuments%2Fmyaerospacecatalog-documents%2FDefense_Brochures-documents%2FMagnetic__Literature_Application_notes-documents%2FAN203_Compass_Heading_Using_Magnetometers.pdf&ei=snYzU9H9B4K52wWu6YCYAw&usg=AFQjCNEAdcpIvR7dYFh6il_kAS1Labah5g&sig2=y1sx6QN30KCnIrXfAtJbhA
                #google "get compass direction from magnetometer"
                if hy>0:
                    dirc = 90.0-np.arctan(hx/hy)*180/np.pi
                elif hy<0:
                    dirc = 270.0-np.arctan(hx/hy)*180/np.pi
                else:
                    dirc = 180.0 if hx > 0 else 0.0
                #90 -> N
                #180-> E
                #270-> S
                #360-> W
                
                dircname = None
                if np.fabs(dirc - 90) <= 22.5:
                    dircname = "North"
                elif np.fabs(dirc - 135) <= 22.5:
                    dircname = "North-East"
                elif np.fabs(dirc - 180) <= 22.5:
                    dircname = "East"
                elif np.fabs(dirc - 225) <= 22.5:
                    dircname = "South-East"
                elif np.fabs(dirc - 270) <= 22.5:
                    dircname = "South"
                elif np.fabs(dirc - 315) <= 22.5:
                    dircname = "South-West"
                elif np.fabs(dirc - 360) <= 22.5:
                    dircname = "West"
                elif np.fabs(dirc - 0) <= 22.5:
                    dircname = "West"
                
                mem[i] = dircname
            except IndexError as e:
                pass #print e
            
        return Counter(mem).most_common(1)[0][0]
    
    def getdirc2(self):
        data, addr = self.sock.recvfrom(1024)
        return data

    """
    Same as getdirc, does not convert degrees to compass heading
    """
    def getdirc3(self):
        n=5
        memsum = 0
        for i in range(n): #get mode of n samples
            try:
                data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
                vect = data.split(",")
                acc = vect[2:5]    #accelerometer
                gyr = vect[6:9]    #gyroscope
                mag = vect[10:14]  #magnetometer readings
                
                #Use hx (i.e. mag[0]) and hy (i.e. mag[1])
                # to get dir as degrees 
                hx = float(mag[0])
                hy = float(mag[1])
                dirc = None
                
                if hy>0:
                    dirc = 90.0-np.arctan(hx/hy)*180/np.pi
                elif hy<0:
                    dirc = 270.0-np.arctan(hx/hy)*180/np.pi
                else:
                    dirc = 180.0 if hx > 0 else 0.0
                memsum += dirc
            except IndexError as e:
                pass #print e
            
        return memsum/n

    def readimu(self):
        data, addr = self.sock.recvfrom(1024)
        return np.array(data.split(","))

    def getacc(self):
        data, addr = self.sock.recvfrom(1024)
        vect = data.split(",")
        acc = map(float, vect[2:5]) #accelerometer
        if len(acc) != 3: acc=[0,0,0]
        return np.array(acc)

    def getgyr(self):
        data, addr = self.sock.recvfrom(1024)
        vect = data.split(",")
        gyr = map(float, vect[6:9])#gyroscope
        if len(gyr) != 3: gyr=[0,0,0]
        return np.array(gyr)

    def getmag(self):
        data, addr = self.sock.recvfrom(1024)
        vect = data.split(",")
        mag = map(float, vect[10:14]) #magnetometer
        if len(mag) != 3: mag=[0,0,0]
        return np.array(mag)




codemap =  { \
      0:' ', #delimit words \
      2:'D', #delete last char \
     13:'a', \
    131:'b', \
    100:'c', \
     22:'d', \
     10:'e', \
    103:'f', \
    133:'g', \
     20:'h', \
     31:'i', \
    112:'j', \
    102:'k', \
     23:'l', \
    101:'m', \
     33:'n', \
     30:'o', \
    113:'p', \
    120:'q', \
     21:'r', \
     12:'s', \
     11:'t', \
     32:'u', \
    130:'v', \
    110:'w', \
    121:'x', \
    111:'y', \
    122:'z', \
    300:'0', \
    301:'1', \
    303:'2', \
    310:'3', \
    311:'4', \
    313:'5', \
    330:'6', \
    331:'7', \
    333:'8', \
    123:'9'}    

def keyer(imu):
    oldenum = -1
    menum = -1
    out = lambda x: speak(x)
    
    #           0                        1                          2               3  
    mmap = ["Rotated Clockwise", "Rotated Counter-Clockwise", "Tail Lifted Up", "Head Lifted Up", "Flat"]
    lastevent = datetime.datetime.now()
    chain = []
    string = []
    #http://stackoverflow.com/questions/489999/python-convert-list-of-ints-to-one-number
    list2num = lambda numList: int(''.join(map(str,numList)))
    
    while True:
        acc = imu.getacc()        
        midx = np.absolute(acc).argmax()

        if midx == 0: #X-axis
            if acc[midx] < 0: 
                menum = 0
                lastevent = datetime.datetime.now()
            else:
                menum = 1
                lastevent = datetime.datetime.now()
        elif midx == 1: #Y-axis
            if acc[midx] < 0: 
                menum = 2
                lastevent = datetime.datetime.now()
            else:
                menum = 3
                lastevent = datetime.datetime.now()
        else: #Z-axis
            menum = 4
            delta = (datetime.datetime.now() - lastevent)   
            milli = delta.seconds * 1000 + delta.microseconds/1000.0
            #print "ms is {}".format(milli)
            if milli > 900: #break sequence after 0.8 second 
                if chain:
                    print "chain is {}".format(chain)
                    try:

                        char = codemap[list2num(chain)]
                        print "char is {}".format(char)
                        
                        #Logic for outputing words                    
                        string.append(char)
                        if char == " ":
                            word = "".join(string) 
                            out(word)
                            print "word is {}".format(word)
                            string = []
                        elif char == "D":
                            try:
                                string.pop()
                                string.pop()
                            except IndexError:
                                pass
                        
                    except KeyError:
                        print "KeyError in keyed value" 
 
                    chain = []
                
        if menum != oldenum:
            oldenum = menum
            if menum!=4:
                chain.append(menum)
            #print mmap[menum]
        
if __name__ == '__main__':
    ipaddr = getIPAddr() #of this machine
    port = 5005
    imu = PhoneIMU(ipaddr=ipaddr,port=port)
    print "Listening on {}:{}".format(ipaddr,port)
    
    """
    print "Compass Direction is: ", imu.getdirc3()
    oldval = None
    newval = None
    """
    
    """
    while True:
        print " ".format(imu.getdirc2())        
        newval = imu.getdirc()
        if newval != oldval and newval != None:
            nav = "Compass Direction is {}".format(newval)
            oldval = newval
            #speak(nav)
            print nav
    """
    #while True: print imu.getacc()
    keyer(imu)

    
    
