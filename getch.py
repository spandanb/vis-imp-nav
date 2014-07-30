import sys
import select

class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        #slight modification to exit on Esc
        ch = self.impl()
        return ch
        """
        if ord(ch)==27:
            import sys
            sys.exit()
        else:
            return ch 
        """

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()
    

def heardEnter():
    i,o,e = select.select([sys.stdin],[],[],0.01)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline()
            return input
    return False    
    
    
if __name__ == '__main__':
    """
    getch = _Getch()
    while True:
        ch = getch()
        if ord(ch) == 27:
            sys.exit()
        else:
            print "User entered {}".format(ch)
    """
    while True:
        resp = heardEnter()
        if resp:
            print "User entered {}".format(resp)