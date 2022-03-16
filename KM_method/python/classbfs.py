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


    def maxMatch_long(self):
        for i in range(self.nx):
            self.S  = [0 for _ in range(self.maxn)]
            self.T  = [0 for _ in range(self.maxn)]
            self.bfs_o4_long(i) 

    def bfs_o4_long(self, xstart):
        find = 0;          
        endY = -1;
        pre  =  [-1 for _ in range(self.maxn)]
        queue = [ 0 for _ in range(self.maxn)]
        qs = 0          # queue index
        qe = 0  

        queue[qe] = xstart
        qe += 1
        while True:
            while (qs < qe and not find):
                x = queue[qs]
                qs += 1
                self.S[x] = 1
                for y in range(self.ny):
                    tmp = self.xl[x] + self.yl[y] + self.g[x][y]
                    
                    if not tmp:
                        if self.T[y]: continue
                        self.T[y] = 1
                        pre[y] = x 
                        if (self.cy[y] == -1):
                            endY = y
                            find = 1
                            break
                        else: 
                            queue[qe] = self.cy[y]
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
                    queue[qe] = i
                    qe += 1
                if self.T[i]:
                    self.yl[i] += self.a
            self.a = 1e8
      
        count = 0
        while endY != -1:
            preX = pre[endY]
            preY = self.cx[preX]
            self.cx[preX] = endY
            self.cy[endY] = preX
            endY = preY
            count += 1

    def maxMatch_short(self): 
        for i in range(1, self.nx):
            self.S  = [0 for _ in range(self.maxn)]
            self.T  = [0 for _ in range(self.maxn)]
            self.bfs_o4_short(i) 


    def bfs_o4_short(self, xstart):
        x  = 0
        y  = 0
        yy = 0
        self.a = 0
        pre   = [  0 for _ in range(self.maxn)]
        slack = [1e8 for _ in range(self.maxn)]
        queue = [ -1 for _ in range(self.maxn)]
        queue[y] = xstart
        
        while True:
            x = queue[y]
            self.a = 1e8
            self.T[y] = True   
            for i in range(1, self.maxn):
                if not self.T[i]:
                    if slack[i] > self.xl[x] + self.yl[i] + self.g[x][i]:
                        slack[i] = self.xl[x] + self.yl[i] + self.g[x][i]
                        pre[i] = y
                    if slack[i] > self.a:
                        self.a = slack[i]
                        yy = i
            for i in range(1, self.maxn):
                if self.T[i]:
                    self.xl[queue[i]] -= self.a
                    self.yl[i] += self.a                
                else:
                    slack[i] -= self.a
            y = yy
            if queue[y]  == -1:
                break
        while y:
            queue[y] = queue[pre[y]]
            y = pre[y]     


    def KuhnMunkres(self):
        # initialization
        self.AllocateArrays()
        # pairing
        if self.mode == 'long':
            self.maxMatch_long()
        elif self.mode == 'short':
            self.maxMatch_short()
        else:
            print("Wrong mode, bye.")
        # results
        self.min_cost = 0 
        for i in range(self.nx):
        #    print("{} -> {}".format(i+1, self.cx[i]+1))
            self.min_cost += self.g[i][self.cx[i]]

