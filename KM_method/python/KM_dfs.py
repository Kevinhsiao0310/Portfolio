import numpy as np, scipy as sp
import os, sys
from numpy import random 

# Kuhn-Munkres Method
class Assignment():

    def __init__(self, nx, ny, cost_matrix, algo):

        #list
        self.g  = cost_matrix
        self.cx = None                   # x_connect
        self.cy = None                   # y_connect        
        self.xl = None                   # y_label
        self.yl = None                   # x_label
        self.S  = None                   # S class
        self.T  = None                   # T class
        self.Ypre   = None
        self.queue  = None
        self.Yslack = None

        #param
        self.nx = nx                     # num of x
        self.ny = ny                     # num of y
        self.a  = 0                      # change of label
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

    def dfs(self, u):

        self.S[u] = 1
        for v in range(self.ny):
            if self.T[v]: 
                continue  
            tmp = self.xl[u] + self.yl[v] + self.g[u][v]
            if tmp == 0: 
                self.T[v] = 1
                if self.cy[v] == -1 or self.dfs(self.cy[v]):
                    self.cx[u] = v
                    self.cy[v] = u
                    return 1
            else:
                self.a = min(tmp, self.a)

        return 0

    def maxMatch(self):

        for i in range(self.nx):
            self.S  = [0 for _ in range(self.maxn)]
            self.T  = [0 for _ in range(self.maxn)]
            self.a  = np.iinfo(np.int32).max

            while(self.dfs(i) == 0):
                for j in range(self.maxn):
                    if self.S[j]: self.xl[j] -= self.a
                    if self.T[j]: self.yl[j] += self.a

                self.S  = [0 for _ in range(self.maxn)]
                self.T  = [0 for _ in range(self.maxn)]
                self.a = np.iinfo(np.int32).max

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
        
        #print("min cost: {}".format(self.min_cost))
 
