import numpy as np, scipy as sp
import os, sys
from numpy import random 

# Kuhn-Munkres Method
class Assignment():

    def __init__(self, nx, ny, cost_matrix, algo, random=0):
        #list
        self.g  = None
        self.cx = None # x_connect
        self.cy = None # y_connect        
        self.xl = None # y_label
        self.yl = None # x_label
        self.S  = None # S class
        self.T  = None # T class
        self.queue = None
        self.cost_matrix = cost_matrix

        #param
        self.nx   = nx   # num of x
        self.ny   = ny   # num of y
        self.a    = 0    # change of label
        self.maxn = max(self.nx, self.ny) + 1
        self.random   = random
        self.min_cost = 0
        self.mode     = algo

    def AllocateArrays(self):
        self.cx = [-1] * self.maxn
        self.cy = [-1] * self.maxn
        self.xl = [-1e8] * self.maxn
        self.yl = [0] * self.maxn
        self.queue = [-1] * self.maxn
        self.g = np.zeros([self.maxn, self.maxn])
 
        for i in range(1, self.maxn):
            for j in range(1, self.maxn):
                a = self.cost_matrix[i-1][j-1] 
                self.g[i][j] = a

        # fill task matrix
        for i in range(1, self.maxn):
            for j in range(1, self.maxn):
                if self.g[i][j] > self.xl[i]:
                    self.xl[i] = self.g[i][j]


    def maxMatch_short(self): 
        for i in range(1, self.maxn):
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
        self.queue[y] = xstart
        
        while True:
            x = self.queue[y]
            self.a = 1e8
            self.T[y] = True   
            for i in range(1, self.maxn):
                if not self.T[i]:
                    if slack[i] > self.xl[x] + self.yl[i] + self.g[x][i]:
                        slack[i] = self.xl[x] + self.yl[i] + self.g[x][i]
                        pre[i] = y
                    if slack[i] < self.a:
                        self.a = slack[i]
                        yy = i
#                print("xl[{}] = {}, yl[{}] = {}, g[{}][{}] = {}, delta = {}".format(x, self.xl[x], i, self.yl[i], x, i, self.g[x][i], self.a))
            for i in range(0, self.maxn):
                if self.T[i]:
                    self.xl[self.queue[i]] -= self.a
                    self.yl[i] += self.a               
#                    print("label changed.! delta = {}, i = {}".format(self.a, i)) 
                else:
                    slack[i] -= self.a
            y = yy
            if self.queue[y]  == -1:
#                print("break while")
                break
        while y:
            self.queue[y] = self.queue[pre[y]]
            y = pre[y]     


    def KuhnMunkres(self):
        # initialization
        self.AllocateArrays()
        # pairing
        if self.mode == 'short':
            self.maxMatch_short()
        else:
            print("Wrong mode, bye.")
        # results
        self.min_cost = 0 
        for i in range(1, self.maxn):
        #    print("{} -> {}".format(i+1, self.cx[i]+1))
            if self.queue[i] != -1:
                self.min_cost += self.g[self.queue[i]][i]

