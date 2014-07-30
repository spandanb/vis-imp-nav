#!/usr/bin/python
from getch import _Getch
import threading
import time


class UserInput (threading.Thread):
    def __init__(self, res):
        threading.Thread.__init__(self)
        self.res = res
        self.getch = _Getch()
        self.runloop = True
    
    def stoploop():
        self.runloop = False
        
    def run(self):
        while self.runloop:
            self.res[0] = read(self.getch)
    
    def get(self):
        return self.res[0]    

def read(getch):
    return getch()
        
if __name__ == "__main__":
    res = [None]
    
    # Create new threads
    thread1 = UserInput(res)
    # Start new Threads
    thread1.start()
    
    while True:
        
        ch = thread1.get() #res[0]        
        if type(ch) == str:
            print "{} {}".format(ch, len(ch))
            res[0] = None
        #thread1        