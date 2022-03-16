import numpy as np
from numpy import random
import sys
from KM_bfs_o4_long import Assignment as KM_bfs_long
from KM_bfs_o4_short import Assignment as KM_bfs_short
from KM_bfs_o3 import Assignment as KM_bfs_o3
from KM_dfs import Assignment as KM_dfs
from hungary import TaskAssignment
import time

L = 300

for j in range(1000):
    print("===== seed: {} =====".format(j))

    rd = random.RandomState(j)
    task_matrix = rd.randint(0, 1000000, size=(L, L)) 

    tstart = time.time()
    ass_by_Hun = TaskAssignment(task_matrix, 'Hungary')
    tend = time.time()
    print("scipy: {} s".format(tend - tstart))

    time.sleep(1)

    a_KP_long = KM_bfs_long(L, L, task_matrix, 'long')
    tstart = time.time()
    a_KP_long.KuhnMunkres()
    tend = time.time()
    print("bfs_long: {} s".format(tend - tstart))

    time.sleep(1)

    KP_short = KM_bfs_short(L, L, task_matrix, 'short')
    tstart = time.time()
    KP_short.KuhnMunkres()
    tend = time.time()
    print("bfs_short: {} s".format(tend - tstart))

    time.sleep(1)

    a_KP_o3 = KM_bfs_o3(L, L, task_matrix, 'o3')
    tstart = time.time()
    a_KP_o3.KuhnMunkres()
    tend = time.time()
    print("bfs_o3: {} s".format(tend - tstart))

    time.sleep(1)

    a_KP_dfs = KM_dfs(L, L, task_matrix, "dfs")
    tstart = time.time()
    a_KP_dfs.KuhnMunkres()
    tend = time.time()
    print("dfs: {} s".format(tend - tstart))


    if ass_by_Hun.min_cost != a_KP_dfs.min_cost:
        print ("ERROR dfs_o4")
        print ("len:", L, "seed:", j, "pylib:", ass_by_Hun.min_cost, "KP:",  a_KP_dfs.min_cost)
    if ass_by_Hun.min_cost != a_KP_long.min_cost:
        print ("ERROR bfs_o4 long") 
        print ("len:", L, "seed:", j, "pylib:", ass_by_Hun.min_cost, "KP:",  a_KP_long.min_cost)
    if ass_by_Hun.min_cost != KP_short.min_cost:
        print ("ERROR bfs_o4 short") 
        print ("len:", L, "seed:", j, "pylib:", ass_by_Hun.min_cost, "KP:",  KP_short.min_cost)
    if ass_by_Hun.min_cost != a_KP_o3.min_cost:
        print ("ERROR bfs_o3") 
        print ("len:", L, "seed:", j, "pylib:", ass_by_Hun.min_cost, "KP:",  a_KP_o3.min_cost)
    else:
        print ("SOLVED")
        #print ("g = \n", task_matrix)
        #print ("mincost = ", a_KP.min_cost)
     
