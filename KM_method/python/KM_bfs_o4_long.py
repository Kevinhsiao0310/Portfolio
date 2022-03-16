import numpy as np, scipy as sp
import os, sys
from numpy import random 

# Kuhn-Munkres Method
class Assignment():

    def __init__(self, nx, ny, cost_matrix, algo):

        #list
        self.g  = cost_matrix
        self.cx = None                       # x_connect
        self.cy = None                       # y_connect        
        self.xl = None                       # y_label
        self.yl = None                       # x_label
        self.S  = None                       # S class
        self.T  = None                       # T class
        self.Yslack = None
        self.queue  = None
        self.Ypre   = None

        #param
        self.nx   = nx                       # num of x
        self.ny   = ny                       # num of y
        self.a    = 0                        # change of label
        self.maxn = max(self.nx, self.ny)
        self.min_cost = 0
        self.mode = algo

    def AllocateArrays(self):
        self.cx = self.maxn * [-1]
        self.cy = self.maxn * [-1]
        self.xl = self.maxn * [np.iinfo(np.int32).min] 
        self.yl = self.maxn * [0] 
        self.S  = self.maxn * [0]
        self.T  = self.maxn * [0]

        # fill task matrix
        for i in range(self.nx):
            for j in range(self.ny):
                if self.g[i][j] > self.xl[i]:
                    self.xl[i] = self.g[i][j]


    def maxMatch(self):
        for i in range(self.nx):
            self.S = [0 for _ in range(self.maxn)]
            self.T = [0 for _ in range(self.maxn)]
            self.Ypre   = [-1 for _ in range(self.maxn)]
            self.queue = [ 0 for _ in range(self.maxn)]
            self.bfs_o4(i) 

    def bfs_o4(self, xstart):
        find = 0;          
        endY = -1;
        qs = 0          # queue index
        qe = 0  

        self.queue[qe] = xstart
        qe += 1
        while True:
            while (qs < qe and not find):
                x = self.queue[qs]
                qs += 1
                self.S[x] = 1
                for y in range(self.ny):
                    tmp = self.xl[x] + self.yl[y] + self.g[x][y]
                    if not tmp:
                        if self.T[y]: continue
                        self.T[y] = 1
                        self.Ypre[y] = x 
                        if (self.cy[y] == -1):
                            endY = y
                            find = 1
                            break
                        else: 
                            self.queue[qe] = self.cy[y]
                            qe += 1
                    else:
                        self.a = min(self.a, tmp)
            if find: 
                break
 
            qs = 0
            qe = 0
            for i in range(self.maxn):
                if self.S[i]:
                    self.xl[i] -= self.a
                    self.queue[qe] = i
                    qe += 1
                if self.T[i]:
                    self.yl[i] += self.a
            self.a = np.iinfo(np.int32).max
      
        while endY != -1:
            preX = self.Ypre[endY]
            preY = self.cx[preX]
            self.cx[preX] = endY
            self.cy[endY] = preX
            endY = preY

    def KuhnMunkres(self):
        # initialization
        self.AllocateArrays()
        # pairing
        self.maxMatch()
        # results
        self.min_cost = 0 
        for i in range(self.nx):
        #    print("{} -> {}".format(i+1, self.cx[i]+1))
            self.min_cost += self.g[i][self.cx[i]]

