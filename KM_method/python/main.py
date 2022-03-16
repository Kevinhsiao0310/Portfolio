import numpy as np
from numpy import random
import sys
from classbfs import Assignment as KM_bfs_long
from classbfs_2 import Assignment as KM_bfs_short
from classdfs import Assignment as KM_dfs
from classbfs_o3 import Assignment as KM_bfs_o3
from hungary import TaskAssignment
import time

L = 100

for j in range(10):
    print("===== seed: {} =====".format(j))

    rd = random.RandomState(j)
    task_matrix = rd.randint(0, 1e7, size=(L, L)) 

    tstart = time.time()
    ass_by_Hun = TaskAssignment(task_matrix, 'Hungary')
    tend = time.time()
    print("scipy cost: {} s".format(tend - tstart))

    a_KP_long = KM_bfs_long(L, L, task_matrix, 'long', random=0)
    tstart = time.time()
    a_KP_long.KuhnMunkres()
    tend = time.time()
    print("bfs_long cost: {} s".format(tend - tstart))

    a_KP = KM_bfs_short(L, L, task_matrix, 'short', random=0)
    tstart = time.time()
    a_KP.KuhnMunkres()
    tend = time.time()
    print("bfs_short cost: {} s".format(tend - tstart))

    a_KP_o3 = KM_bfs_o3(L, L, task_matrix, 'o3', random = 0)
    tstart = time.time()
    a_KP_o3.KuhnMunkres()
    tend = time.time()
    print("bfs_o3 cost: {} s".format(tend - tstart))

    task_KP = KM_dfs(L, L, task_matrix, random = 0)
    tstart = time.time()
    task_KP.KuhnMunkres()
    tend = time.time()
    print("dfs cost: {} s".format(tend - tstart))

    if ass_by_Hun.min_cost != a_KP.min_cost or a_KP_o3.min_cost != ass_by_Hun.min_cost or a_KP_long.min_cost != ass_by_Hun.min_cost or ass_by_Hun.min_cost != task_KP.min_cost:
        print ("ERROR")
        print ("len:", L, "seed:", j, "pylib:", ass_by_Hun.min_cost, "KP:",  a_KP.min_cost)

    else:
        print ("SOLVED")
        #print ("g = \n", task_matrix)
        print ("mincost = ", a_KP.min_cost)
     
