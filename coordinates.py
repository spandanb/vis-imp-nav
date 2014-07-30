import socket
import numpy as np

def getIPAddr():
    return socket.gethostbyname(socket.getfqdn()) 

class Coordinates():
    def __init__(self, ipaddr="192.168.0.14", port=5555):
        self.UDP_IP = ipaddr
        self.UDP_PORT = port

        self.sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
        self.sock.bind((self.UDP_IP, self.UDP_PORT))
    
    def getCoord(self, frmt=False):
        data, addr = self.sock.recvfrom(1024)
        if not frmt: #return raw string
            return data
        else: #Return formatted tuple
            return tuple(map(float, data.split(" ")))
    
    #start and end are (lat, long)
    #http://www.movable-type.co.uk/scripts/latlong.html
    def getDistBrng(self, start, end):
        latS  = start[0] #start latitude
        latE  = end[0] #end latitude
        longS = start[1] #start longitude
        longE = end[1] #end longitude
        
        R = 6371 #earth's radius
        dLat = np.radians(longE - longS)
        dLon = np.radians(latE - latS)
        latS = np.radians(latS)
        latE = np.radians(latE)
        
        a = np.sin(dLat/2) * np.sin(dLat/2) + np.sin(dLon/2) * np.sin(dLon/2) * np.cos(latS) * np.cos(latE)
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
        distance = R * c

        y = np.sin(dLon) * np.cos(latE);
        x = np.cos(latS) * np.sin(latE) - np.sin(latS) * np.cos(latE) * np.cos(dLon);
        bearing = np.degrees(np.arctan2(y, x))
        if bearing < 0:
            bearing += 360 
        return (distance, bearing)

    """
    Latitude 
    Equator = 0
    North Pole = 90
    South Pole = -90
    N > S 
    
    Longitude
    Prime Meridian = 0
    Eastward -> +ve
    Westward -> -ve
    E > W
    """
    
    #Bearing to Heading
    def brngToHdng(self, dirc):        
        if dirc < 0:
            dirc += 360        
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
        return dircname
    
if __name__ == "__main__":
    ipaddr = getIPAddr()
    port = 5007
    print "ipaddr:port = {}:{}".format(ipaddr, port)     
    coord = Coordinates(ipaddr=ipaddr, port=port)
    #while True:
    print coord.getCoord()
    borden = (43.65890142, -79.4056563)
    yonge = (43.6546247, -79.3801909)
    dist, brng = coord.getDistBrng(borden, yonge)
    print dist, brng
    print dist, coord.brngToHdng(brng)
    
    #What are tradeoff between partition vs replication
    #Locality
    #Synchronization, WAN vs LAN
    #read-dominated vs write-dominated