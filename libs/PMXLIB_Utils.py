import os, sys, argparse, cv2
import matplotlib.pyplot as plt 
import numpy as np

### FileName Format

class LOGname:
    def __init__(self):
        self.fullname  = None
        self.vname     = None  
        self.AImodel   = None
        self.AIversion = None
        self.res       = None
        self.AIdate    = None
        self.eval      = None
        self.draw      = None
 
    def collectPARAMS(self, vname, AImodel, AIversion, model_w, model_h, AIdate, Eval, draw):
        self.vname     = vname 
        self.AImodel   = AImodel  
        self.AIversion = AIversion
        self.res       = "x".join((model_w, model_h))
        self.AIdate    = AIdate
        self.eval      = str(Eval)
        self.draw      = str(draw)  

    def txtname(self):
        if self.draw == str('draw'):
            seq = (self.vname, self.AImodel, self.AIversion, self.res, self.AIdate, self.eval, self.draw) 
            self.fullname = "_".join(seq)
            self.fullname = self.fullname + ".txt"
        elif self.draw == str('ndraw'):
            seq = (self.vname, self.AImodel, self.AIversion, self.res, self.AIdate, self.eval) 
            self.fullname = "_".join(seq)
            self.fullname = self.fullname + ".txt"
        return self.fullname

class VIDEOname:
    def __init__(self, filename):
        self.fullname  = None
        self.vname     = None  
        self.AImodel   = None
        self.AIversion = None
        self.res       = None
        self.AIdate    = None
        self.draw      = None

    def collectPARAMS(self, vname, AImodel, AIversion, model_w, model_h, AIdate, draw):
        self.vname     = vname 
        self.AImodel   = AImodel  
        self.AIversion = AIversion
        self.res       = "x".join((model_w, model_h))
        self.AIdate    = AIdate
        self.draw      = draw  
     
    def videoname(self):
        seq = (self.vname, self.AImodel, self.AIversion, self.res, self.AIdate, self.draw) 
        self.fullname = "_".join(seq)
        self.fullname = self.fullname + ".mp4"

        return self.fullname

def readLog(log_path, model):
    logname = log_path.split('/')[-1].strip('.txt')
    split = logname.split('_')
    box = LOGname()
    box.collectPARAMS(split[0], split[1], split[2], split[3].split('x')[0], split[3].split('x')[1], split[4], 'Eval', model)
    log_box = box.txtname()
    return box