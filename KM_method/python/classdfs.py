import numpy as np, scipy as sp
import os, sys
from numpy import random 

# Kuhn-Munkres Method
class Assignment():

    def __init__(self, nx, ny, cost_matrix, random=0):
        #list
        self.g  = cost_matrix
        self.cx = None # x_connect
        self.cy = None # y_connect        
        self.xl = None # y_label
        self.yl = None # x_label
        self.S  = None # S class
        self.T  = None # T class

        #param
        self.nx = nx   # num of x
        self.ny = ny   # num of y
        self.a  = 0    # change of label
        self.maxn = max(self.nx, self.ny)
        self.random = random
        self.min_cost = None

    def AllocateArrays(self):
        #self.g = [[0] * self.ny for _ in range(self.nx)]
        self.cx = [0] * self.maxn
        self.cy = [0] * self.maxn
        self.xl = [-1e8] * self.maxn
        self.yl = [0] * self.maxn

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
            temp = self.xl[u] + self.yl[v] + self.g[u][v]
            if temp == 0: 
                self.T[v] = 1
                if self.cy[v] == -1 or self.dfs(self.cy[v]):
                    self.cx[u] = v
                    self.cy[v] = u
                    return 1
            else:
                self.a = min(temp, self.a)

        return 0

    def maxMatch(self):
        res = 0 
        self.cx = [-1 for _ in range(self.nx)]
        self.cy = [-1 for _ in range(self.ny)]

        for i in range(self.nx):
            self.S  = [0 for _ in range(self.maxn)]
            self.T  = [0 for _ in range(self.maxn)]
            self.a  = 1e8

#            print("finding path for node:{}".format(i))
            while(self.dfs(i) == 0):
                self.labelchange()
                self.S  = [0 for _ in range(self.maxn)]
                self.T  = [0 for _ in range(self.maxn)]
                self.a = 1e8

    def labelchange(self):
        for i in range(self.maxn):
            if self.S[i]: self.xl[i] -= self.a
            if self.T[i]: self.yl[i] += self.a

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
 
#rd = random.RandomState()
#task_matrix = rd.randint(0, 100, size=(3, 3))
#a = Assignment(3, 3, task_matrix, random=0)
#a.KuhnMunkres()
