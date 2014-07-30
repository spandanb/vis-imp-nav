#!/usr/bin/python

import cv2.cv as cv
import cv2
import numpy as np
import re
import subprocess as sp
import glob
import re
import os
import sys
import time
import video
import json
import urllib


debug = [True, False] #debug, verbose

#validChars = re.compile("[\w.:?- ]")
validChars = re.compile("[\w.? ]")
alphaNum = re.compile("[0-9A-Za-z ]")

"""
@params
    s-input string
"""
def removeNonRenderable(s):
    return "".join(i for i in s if ord(i)<128 and ord(i)>10)

def speak(arg, pr=True):
    if isinstance(arg, str):
        cmd =  ["say", arg ]
    elif isinstance(arg, list):
        cmd=["say"] + arg
    else:
        cmd = None
        print "Error: Unknown arg type"
    if cmd:
        removeNoneAlphaNum = lambda word: "".join(i for i in word if re.search(alphaNum, i))
        cmd = map(removeNoneAlphaNum, cmd)
        
        if pr: print "Speaking {}".format(" ".join(cmd))
        sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
        
"""
pass dir name
"""
def getImgName(dir):
    if dir[-1] != "/":
        dir += "/"
    files = glob.glob(dir+"out[0-9]*.jpg")
    maxnum = -1
    for f in files:
        num = int(re.search("[0-9]+", f[len(dir):]).group(0))
        if num>maxnum : maxnum = num
    return dir + "out{}.jpg".format(maxnum+1)
        
def getGoogleHits(query):    
    query = "".join(i for i in query if re.search(validChars, i) )
    if len(query) < 3: return 0 #Do not process garabage queries
    
    query = urllib.urlencode({'q': query})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
    search_response = urllib.urlopen(url)
    search_results = search_response.read()
    results = json.loads(search_results)
    data = results['responseData']
    if debug[1]: print "data is {}".format(data)
    try:
        hits = int(data['cursor']['estimatedResultCount'])
    except (KeyError, TypeError) as e:
        hits = sum(map(len, query))
    if debug[1]: print "Query is {}, hits are {}".format(query, hits)
    return hits

#TODO: For performance, make multithreaded
if __name__ == '__main__':
    cam = video.create_capture(0) #cv2.VideoCapture(0)
    ret, img = cam.read()
    takephoto = False
    imgdir = "./img/" #out.jpg" #path of outputfile
    textFile = "outtext/out"
    textFileExt = "outtext/out.txt"
    imgfile = imgdir + "out.jpg"
    
    start = False #Used to denote start taking pictures
    startBuffer = 0
    startBufferMax = 10 #step size
    
    cand = [] #candidate texts
    maxHits = 0
    
    startTime = None
    maxTime = 5 #seconds
    
    while True:
        
        ret, img = cam.read() #img is numpy 3-array
        invimg = np.fliplr(img) #inverted 
        
        #Takes one photo
        if takephoto:
            imgfile = getImgName(imgdir)
            cv2.imwrite(imgfile, img) #Write image file            
            #tesseract usage: tesseract <inputfile> <outputfile>
            exitcode = sp.call(["tesseract", imgfile, textFile]) #Recognize
            if exitcode:
                print "Error Occured"
            else:
                text = open(textFileExt).readlines()    
                print filter(lambda s: s,  map(removeNonRenderable, text) )
            takephoto = False    
        
        if start:
            if startBuffer == startBufferMax:
                #imgfile = imgdir + "out.jpg"
                cv2.imwrite(imgfile, img) #Write image file            
                #tesseract usage: tesseract <inputfile> <outputfile>                
                p = sp.Popen(["tesseract", imgfile, textFile], stdout=sp.PIPE, stderr=sp.PIPE)
                if p.returncode:
                    print "Error Occured"
                else:
                    text = open(textFileExt).readlines() #list of strings
                    renderable = map(removeNonRenderable, text) #Renderable characters
                    clean = filter(lambda s: s.strip() , renderable ) #non empty and non space characters
                    if debug[0]: print "clean is {}, cand is {}".format(clean, cand)
                    if clean: 
                        hits = map(getGoogleHits, clean)
                        if debug[0]: print "hits is {}".format(hits)
                        val = sum(hits)#np.mean(hits)
                        print val
                        if val > maxHits:
                            maxHits = val
                            cand = clean
                startBuffer -= 1    
            elif startBuffer == 0:
                startBuffer = startBufferMax
            else:
                startBuffer -=1    
        
            if time.time() - startTime > maxTime and maxHits > 0: #End loop
                start = False
                speak("Ending recognition.")
                if cand:                      
                    speak(cand)
        cv2.imshow('img', img )
        

        key = cv.WaitKey(10)
        if key == 27:
            break
        elif key == ord('x'): #Single photo
            takephoto = True
        elif key == ord('z'): #Best guess
            speak("Starting recognition")
            start = not start
            startBuffer = startBufferMax
            cand = []
            startTime = time.time()
            maxHits = 0
        elif key == ord('r'):
            if cand: speak(cand)
    
    cv.DestroyAllWindows()
    #os.remove(imgfile)
    #os.remove(textFileExt)
 
