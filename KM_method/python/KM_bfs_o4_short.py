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
        self.cost_matrix = cost_matrix

        #param
        self.nx   = nx                       # num of x
        self.ny   = ny                       # num of y
        self.a    = 0                        # change of label
        self.maxn = max(self.nx, self.ny) + 1
        self.min_cost = 0 
        self.mode = algo

    def AllocateArrays(self):
        self.cx = self.maxn * [-1]
        self.cy = self.maxn * [-1]
        self.xl = self.maxn * [np.iinfo(np.int32).min] 
        self.yl = self.maxn * [0] 
        self.S  = self.maxn * [0] 
        self.T  = self.maxn * [0]
        self.queue = self.maxn * [-1]

        self.g = np.zeros([self.maxn, self.maxn])

        # fill task matrix
        for i in range(1, self.maxn):
            for j in range(1, self.maxn):
                a = self.cost_matrix[i-1][j-1] 
                self.g[i][j] = a 

        for i in range(1, self.nx):
            for j in range(1, self.ny):
                if self.g[i][j] > self.xl[i]:
                    self.xl[i] = self.g[i][j]

    def maxMatch(self): 
        for i in range(1, self.maxn):
            self.S  = [0 for _ in range(self.maxn)]
            self.T  = [0 for _ in range(self.maxn)]
            self.Ypre   = [0 for _ in range(self.maxn)]
            self.Yslack = [np.iinfo(np.int32).max for _ in range(self.maxn)]
            self.bfs_o4(i) 


    def bfs_o4(self, xstart):
        x  = 0
        y  = 0
        yy = 0
        self.a = 0
        self.queue[y] = xstart
        
        while True:
            x = self.queue[y]
            self.a = np.iinfo(np.int32).max
            self.T[y] = True   
            for i in range(1, self.maxn):
                if not self.T[i]:
                    if self.Yslack[i] > self.xl[x] + self.yl[i] + self.g[x][i]:
                        self.Yslack[i] = self.xl[x] + self.yl[i] + self.g[x][i]
                        self.Ypre[i] = y
                    if self.Yslack[i] < self.a:
                        self.a = self.Yslack[i]
                        yy = i
            for i in range(0, self.maxn):
                if self.T[i]:
                    self.xl[self.queue[i]] -= self.a
                    self.yl[i] += self.a               
                else:
                    self.Yslack[i] -= self.a
            y = yy
            if self.queue[y]  == -1:
                break
        while y:
            self.queue[y] = self.queue[self.Ypre[y]]
            y = self.Ypre[y]     


    def KuhnMunkres(self):
        # initialization
        self.AllocateArrays()
        # pairing
        self.maxMatch()
        # results
        self.min_cost = 0 
        for i in range(1, self.maxn):
        #    print("{} -> {}".format(i+1, self.cx[i]+1))
            if self.queue[i] != -1:
                self.min_cost += self.g[self.queue[i]][i]
