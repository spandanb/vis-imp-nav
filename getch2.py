import sys, tty, termios
import select

class _Getch: #Only works on *ix
    def __init__(self):
        pass

    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ord(ch) == 27: sys.exit(0)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def fetch():
    i,o,e = select.select([sys.stdin],[],[],0.01)    
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline()
            return input
    return False    
    

class Getch(): #Non-blocking
    def __init__(self):
        pass
    
    def __call__(self):
        #timeout in seconds; smaller number -> less blocking   
        timeout = 0.01 #1/100 of seconds
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)        
        ch = False
        try:
            tty.setraw(sys.stdin.fileno())
            i,o,e = select.select([sys.stdin],[],[],timeout)
            for s in i:
                if s == sys.stdin:            
                    ch = sys.stdin.read(1)
                    if ord(ch) == 27: sys.exit(0)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch



    
if __name__ == '__main__':
    
    """
    getch = Getch()
    while True:
        ch = getch()
        if ch:
            if ord(ch) == 27:
                sys.exit()
            else:
                print "User entered {}".format(ch)
        else:
            pass #print "blank"
    """

    while True:
        resp = fetch()
        if resp:
            print "User entered {}".format(resp[0])
