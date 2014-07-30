from getch import _Getch
from threading import Thread

getch = _Getch()
#s = getch()

def read(res):
    res[0]=getch()

class UserInput():
    def __init__(self, ):
        self.getch = _Getch()
        self.userinp = [None]
        self.thrd = Thread(target=self.readinp, args=(self, self.userinp))
        self.thrd.start()
            
    #def start(self):
    #    self.thrd.start()
    
    def readinp(self, res):
        while True:
            res[0] = self.getch()
    
    def get(self):
        return self.userinp[0]





if __name__ == '__main__':
    #u = UserInput()
    #u.get()
    
    res = [None]
    t = Thread(target=read, args=(res))
    t.start()
    while True:
        print t.get()