#!/usr/bin/python3
import os
from matplotlib import pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

class timetable():
    def __init__(self):
        self.scipy     = []
        self.bfs_long  = []
        self.bfs_short = []
        self.bfs_o3    = []
        self.dfs       = []

    def convertnp(self):
        self.scipy     = np.array(self.scipy)
        self.bfs_long  = np.array(self.bfs_long)
        self.bfs_short = np.array(self.bfs_short)
        self.bfs_o3    = np.array(self.bfs_o3)
        self.dfs       = np.array(self.dfs)

    def checklist(self):
        print(" LEN: scipy:{}, bfs_long:{}, bfs_short:{}, bfs_o3:{}, dfs:{}".format(len(self.scipy), len(self.bfs_long), len(self.bfs_short), len(self.bfs_o3), len(self.dfs)))
        print(" MAX: scipy:{:2f}, bfs_long:{:2f}, bfs_short:{:2f}, bfs_o3:{:2f}, dfs:{:2f}".format(np.max(self.scipy), np.max(self.bfs_long), np.max(self.bfs_short), np.max(self.bfs_o3), np.max(self.dfs)))

def loadtxt(log_path): 

    time = timetable()        

    if os.path.isfile(log_path):
        print(" Load LOG {}".format(log_path))
        fp = open(log_path, "r")
        lines = fp.readlines()

        for line in lines:
            line = line.strip('\n')
            split = line.split(" ")
            head = split[0]
            tail = split[-1]
            num  = float(split[-2])
            if tail == "s":
                if head == "scipy:":
                    time.scipy.append(num)
                elif head == "bfs_long:": 
                    time.bfs_long.append(num)
                elif head == "bfs_short:":
                    time.bfs_short.append(num)
                elif head == "bfs_o3:":
                    time.bfs_o3.append(num)
                elif head == "dfs:":
                    time.dfs.append(num)
        fp.close()

    return time


t = loadtxt('LOG')
t.convertnp()
t.checklist()




plt.hist(np.array(t.scipy),     bins = 50,  label = 'scipy')
plt.hist(np.array(t.bfs_short), bins = 50,  label = 'bfs_short')
plt.hist(np.array(t.bfs_o3),    bins = 50,  label = 'bfs_o3')
plt.hist(np.array(t.dfs),       bins = 500, label = 'dfs')
plt.xticks(np.arange(0, 200, 50))
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.xlim(0, 100)
plt.ylim(0, 70)
plt.xlabel('time cost')
plt.ylabel('histogram')
plt.legend()
plt.show()
