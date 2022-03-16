import itertools
import numpy as np
from numpy import random
from scipy.optimize import linear_sum_assignment
import sys
 
# 任務分配類
class TaskAssignment:
 
    # 類初始化，需要輸入參數有任務矩陣以及分配方式，其中分配方式有兩種，全排列方法all_permutation或匈牙利方法Hungary。
    def __init__(self, task_matrix, mode):
        self.task_matrix = task_matrix
        self.mode = mode
        self.row = None
        self.col = None
        if mode == 'all_permutation':
            self.min_cost, self.best_solution = self.all_permutation(task_matrix)
        if mode == 'Hungary':
            self.min_cost, self.best_solution, self.row, self.col = self.Hungary(task_matrix)
 
    # 全排列方法
    def all_permutation(self, task_matrix):
        number_of_choice = len(task_matrix)
        solutions = []
        values = []
        for each_solution in itertools.permutations(range(number_of_choice)):
            each_solution = list(each_solution)
            solution = []
            value = 0
            for i in range(len(task_matrix)):
                value += task_matrix[i][each_solution[i]]
                solution.append(task_matrix[i][each_solution[i]])
            values.append(value)
            solutions.append(solution)
        min_cost = np.min(values)
        best_solution = solutions[values.index(min_cost)]
        return min_cost, best_solution
 
    # 匈牙利方法
    def Hungary(self, task_matrix):
        #print("row", len(task_matrix))
        if len(task_matrix) == 1:
            col_ind = np.argmin(task_matrix)
            #print(col_ind)
            min_cost = task_matrix[0][col_ind]
            best_solution = [task_matrix[0][col_ind]]
            return min_cost, best_solution, [0], [col_ind]

        b = task_matrix.copy()
        # 行和列減0
        for i in range(len(b)):
            row_min = np.min(b[i])
            for j in range(len(b[i])):
                b[i][j] -= row_min
        for i in range(len(b[0])):
            col_min = np.min(b[:, i])
            for j in range(len(b)):
                b[j][i] -= col_min
        line_count = 0
        # 線數目小於矩陣長度時，進行循環
        while (line_count < len(b)):
            line_count = 0
            row_zero_count = []
            col_zero_count = []
            for i in range(len(b)):
                row_zero_count.append(np.sum(b[i] == 0))
            for i in range(len(b[0])):
                col_zero_count.append((np.sum(b[:, i] == 0)))
            # 劃線的順序（分行或列）
            line_order = []
            row_or_col = []
            for i in range(len(b[0]), 0, -1):
                while (i in row_zero_count):
                    line_order.append(row_zero_count.index(i))
                    row_or_col.append(0)
                    row_zero_count[row_zero_count.index(i)] = 0
                while (i in col_zero_count):
                    line_order.append(col_zero_count.index(i))
                    row_or_col.append(1)
                    col_zero_count[col_zero_count.index(i)] = 0
            # 畫線覆蓋0，並得到行減最小值，列加最小值後的矩陣
            delete_count_of_row = []
            delete_count_of_rol = []
            row_and_col = [i for i in range(len(b))]
            for i in range(len(line_order)):
                if row_or_col[i] == 0:
                    delete_count_of_row.append(line_order[i])
                else:
                    delete_count_of_rol.append(line_order[i])
                c = np.delete(b, delete_count_of_row, axis=0)
                c = np.delete(c, delete_count_of_rol, axis=1)
                line_count = len(delete_count_of_row) + len(delete_count_of_rol)
                # 線數目等於矩陣長度時，跳出
                if line_count == len(b):
                    break
                # 判斷是否畫線覆蓋所有0，若覆蓋，進行加減操作
                if 0 not in c:
                    row_sub = list(set(row_and_col) - set(delete_count_of_row))
                    min_value = np.min(c)
                    for i in row_sub:
                        b[i] = b[i] - min_value
                    for i in delete_count_of_rol:
                        b[:, i] = b[:, i] + min_value
                    break
        row_ind, col_ind = linear_sum_assignment(b)
        min_cost = task_matrix[row_ind, col_ind].sum()
        best_solution = list(task_matrix[row_ind, col_ind])
        return min_cost, best_solution, row_ind, col_ind
 
