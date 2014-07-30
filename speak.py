import subprocess as sp

def speak(arg):   
    if isinstance(arg, str):
        cmd =  ["say", arg ]
    elif isinstance(arg, list):
        cmd=["say"] + arg
    else:
        cmd = None
        print "Error: Unknown arg type"
    if cmd:
        child = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
        streamdata = child.communicate()[0]
        rc = child.returncode
        return rc  

if __name__ == '__main__':  
    speak("hello")
    speak("world")
          
