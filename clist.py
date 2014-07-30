import numpy as np

class CList():
    def __repr__(self):
        #return self.vect
        oldest = (self.idx+1)%self.size
        return str(self.vect[oldest:] + self.vect[:oldest]) #oldest -> newest
    
    def __init__(self,size):
        self.vect = [None]*size
        self.idx = 0 #where newest element is
        self.size = size 
    
    #Put element in list 
    def push(self, arg):
        self.idx = (self.idx + 1) % self.size
        self.vect[self.idx] = arg        
    
    #Get last element 
    def get(self):
        return self.vect[self.idx] 
    
    #get lastN elements
    def getn(self, n=0, last=False):
        oldest = (self.idx+1)%self.size #oldest index
        if last: #only return first and last index
            return [self.vect[oldest], self.vect[self.idx]]
        
        if n<=0 or n>self.size:
            raise Exception
        
        if n == self.size:            
            return self.vect[oldest:] + self.vect[:oldest]
 
        head = self.vect[:self.idx+1]
        if len(head) >= n:
            firstidx = len(head) - n
            return head[firstidx:]        
        else:
            tail = self.vect[self.idx+1:]
            firstidx = len(tail) - (n-len(head))#first index of tail
            return tail[firstidx:] + head
          
    def raw(self):
        return self.vect