import numpy as np, sys, time
from numpy import random
from KM_bfs_o3 import Assignment as KM_bfs_o3


L = 3
task_matrix = np.array([[37, 12, 72], [9, 75, 5], [79, 64, 16]])

a_KP_o3 = KM_bfs_o3(L, L, task_matrix, 'o3')
tstart = time.time()
a_KP_o3.KuhnMunkres()
tend = time.time()
print("bfs_o3: {} us".format(1000000 * (tend - tstart)))

print ("g = \n", task_matrix)
print ("mincost = ", a_KP_o3.min_cost)
     
