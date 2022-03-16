#!/usr/bin/python3
import os
from matplotlib import pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

class timetable():
    def __init__(self):
        self.bfs = []
        self.dfs = []

    def convertnp(self):
        self.bfs = np.array(self.bfs)
        self.dfs = np.array(self.dfs)

    def checklist(self):
        print(" LEN: bfs:{}, dfs:{}".format(len(self.bfs), len(self.dfs)))
        print(" MAX: bfs:{:2f}, dfs:{:2f}".format(np.max(self.bfs), np.max(self.dfs)))

def loadtxt(log_path): 

    time = timetable()        

    if os.path.isfile(log_path):
        print(" Load LOG {}".format(log_path))
        fp = open(log_path, "r")
        lines = fp.readlines()

        for line in lines:
            line = line.strip('\n')
            split = line.split(" ")
            if "maxMatch_bfs" in split:
                time.bfs.append(float(split[-2])) 
            elif "maxMatch_dfs" in split:
                time.dfs.append(float(split[-2]))
        fp.close()

    return time


t = loadtxt('LOG_n128_s1000_G2_SHORT')
t.convertnp()
t.checklist()

plt.hist(t.dfs, bins = 100, label = 'dfs(Guardian2)', density = 1) 
plt.hist(t.bfs, bins = 100, label = 'bfs(Guardian2)', density = 1)
#plt.hist(t.dfs, bins = 30, label = 'dfs')
#plt.xticks(np.arange(0, 100, 10))
#plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.xlim(0, 4e5)
plt.ylim(0, 1e-4)
plt.xlabel('time cost(us)')
plt.ylabel('histogram')
plt.legend()
plt.show()
