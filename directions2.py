import json, requests
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ' '.join(self.fed).replace("  ", " ")
        
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

prepAddr = lambda addr: addr.strip().replace(" ", "+") 

class Directions():
    def __init__(self, start, end, key="AIzaSyDjc6ZctgLju0LyWXQCH9yiEPHg2ehk_RY"):
        self.start = start
        self.end = end
        self.key = key
        
    def getsteps(self, start=None, end=None):
        url = 'https://maps.googleapis.com/maps/api/directions/json'
        if start:
            self.start = start
        if end:
            self.end = end
            
        params = dict(
            origin      =self.start,
            destination =self.end,
            sensor      ='false',
            mode        ='driving', #'walking'
            key         = self.key,
        )
        self.resp = requests.get(url=url, params=params)        
        js = self.resp.json()
        self.js = js
        tmp = js["routes"]
        tmp = tmp[0]
        tmp = tmp["legs"]
        tmp = tmp[0]
        tmp = tmp["steps"]
        self.steps = tmp #steps vector
        self.parsed_steps = map(lambda raw: str(strip_tags(raw["html_instructions"])), tmp)
        return self.parsed_steps
            
    #Return (lat, long) of destination     
    def getDestCoord(self):
        tmp = self.steps
        tmp = tmp[-1]["end_location"]
        return (tmp["lat"], tmp["lng"])
    
    #Returns coordinates 
    def getStepCoords(self):
        latLon = map(lambda raw: raw["start_location"], self.steps)
        return map(lambda pair: (pair["lat"], pair["lng"]), latLon)
    
if __name__ == "__main__":

    #start = "59 Borden Street, Toronto, ON M5S2M8"
    start = "43.65890142 -79.4056563" #59 Borden
    #start = "40 St George St, Toronto, ON, M5S2E4"
    end = "220 Yonge St, Toronto, ON M5B2H1" #43.6546247 -79.3801909 
    #end = "16 Sifton Place, Brampton, ON, L6Y2N8"
    directions = Directions(start, end) 
    steps = directions.getsteps()
    print steps
    #for d in directions.getDestCoord():
    #    print d
    dc = directions.getDestCoord()
    sc = directions.getStepCoords()
    s = directions.getsteps()
    print sc