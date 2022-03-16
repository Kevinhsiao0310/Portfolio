import numpy as np, scipy as sp
import os, sys
from numpy import random 

# Kuhn-Munkres Method
class Assignment():

    def __init__(self, nx, ny, cost_matrix, algo, random=0):
        #list
        self.g  = cost_matrix
        self.cx = None # x_connect
        self.cy = None # y_connect        
        self.xl = None # y_label
        self.yl = None # x_label
        self.S  = None # S class
        self.T  = None # T class

        #param
        self.nx   = nx   # num of x
        self.ny   = ny   # num of y
        self.a    = 0    # change of label
        self.maxn = max(self.nx, self.ny)
        self.random   = random
        self.min_cost = 0
        self.mode     = algo

    def AllocateArrays(self):
        self.cx = [-1] * self.maxn
        self.cy = [-1] * self.maxn
        self.xl = [-1e8] * self.maxn
        self.yl = [0] * self.maxn

        # fill task matrix
        for i in range(self.nx):
            for j in range(self.ny):
                if self.g[i][j] > self.xl[i]:
                    self.xl[i] = self.g[i][j]


    def maxMatch(self):
        for i in range(self.nx):
            self.S  = [0 for _ in range(self.maxn)]
            self.T  = [0 for _ in range(self.maxn)]
            self.bfs_o3(i) 

    def bfs_o3(self, xstart):
        find = 0;          
        endY = -1;
        pre  =  [-1 for _ in range(self.maxn)]
        queue = [ 0 for _ in range(self.maxn)]
        slack = [ np.iinfo(np.int32).max for _ in range(self.maxn)]
        qs = 0          # queue index
        qe = 0  

        queue[qe] = xstart
        qe += 1
        while not find:
            while (qs < qe and not find):
                x = queue[qs]
                qs += 1
                self.S[x] = 1
                for y in range(self.ny):
                    if self.T[y]:
                        continue
                    tmp = self.xl[x] + self.yl[y] + self.g[x][y]
                    if not tmp:
                        self.T[y] = 1
                        pre[y] = x 
                        if (self.cy[y] == -1):
                            endY = y
                            find = 1
                            break
                        else: 
                            queue[qe] = self.cy[y]
                            qe += 1
                    elif slack[y] > tmp:
                        slack[y] = tmp
                        pre[y] = x
            if find: 
                break

            self.a = np.iinfo(np.int32).max
            for y in range(self.maxn):
                if not self.T[y]:
                    self.a = min(self.a, slack[y])
 
            for i in range(self.maxn):
                if self.S[i]:
                    self.xl[i] -= self.a
                if self.T[i]:
                    self.yl[i] += self.a
            qs = 0
            qe = 0

            for y in range(self.maxn):
                if (not self.T[y] and slack[y] == self.a):
                    self.T[y] = 1
                    if self.cy[y] == -1:
                        endY = y
                        find = 1
                        break
                    else:
                        queue[qe] = self.cy[y]
                        qe += 1
                slack[y] -= self.a
 
        while endY != -1:
            preX = pre[endY]
            preY = self.cx[preX]
            self.cx[preX] = endY
            self.cy[endY] = preX
            endY = preY


    def KuhnMunkres(self):
        # initialization
        self.AllocateArrays()
        # pairing
        if self.mode == 'o3':
            self.maxMatch()
        else:
            print("Wrong mode, bye.")
        # results
        self.min_cost = 0 
        for i in range(self.nx):
        #    print("{} -> {}".format(i+1, self.cx[i]+1))
            self.min_cost += self.g[i][self.cx[i]]

