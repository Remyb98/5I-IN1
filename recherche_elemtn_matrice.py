import random
from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np
import progressbar


def generate_matrice_sorted(line, col):
    M = []
    for i in range(line):
        C = []
        if i > 0:
            max_prec = M[i - 1][col - 1]
        for j in range(col):
            if i > 0:
                val = random.randrange(max_prec, 7 + max_prec)
            else:
                val = random.randrange(1, 7)
            if j > 0:
                while val <= C[j - 1]:
                    val = random.randint(C[j - 1], 7 + C[j - 1])
            C.append(val)
        M.append(C)
    return M


def find_elt_matrix_sort_glout(M, elt):
    iteration = 0
    for i in range(len(M)):
        iteration += 1
        for j in range(len(M[0])):
            iteration += 1
            if M[i][j] == elt:
                return (i, j), iteration
    return None, iteration


def find_elt_matrix_sort_opti(M, elt):
    decal = 0
    size_line = len(M) - 1
    col = len(M[0]) - 1
    iteration = 0
    mid = size_line // 2
    while decal <= size_line:
        iteration += 1
        if M[mid][col // 2] == elt:
            return (mid, col // 2), iteration
        if M[mid][col // 2] > elt:
            if M[mid - 1][col - 1] < elt or mid == 0:
                decal_col = 0
                size_col = len(M[0]) - 1
                mid_col = size_col // 2
                while decal_col <= size_col:
                    iteration += 1
                    if M[mid][mid_col] == elt:
                        return (mid, mid_col), iteration
                    elif M[mid][mid_col] > elt:
                        size_col = mid_col - 1
                    else:
                        decal_col = mid_col + 1
                    mid_col = (decal_col + size_col) // 2
                return None, iteration
            else:
                size_line = mid - 1
        if M[mid][col // 2] < elt:
            if mid == len(M)-1:
                decal_col = 0
                size_col = len(M[0]) - 1
                mid_col = size_col // 2
                while decal_col <= size_col:
                    iteration += 1
                    if M[mid][mid_col] == elt:
                        return (mid, mid_col), iteration
                    elif M[mid][mid_col] > elt:
                        size_col = mid_col - 1
                    else:
                        decal_col = mid_col + 1
                    mid_col = (decal_col + size_col) // 2
                return None, iteration
            if M[mid + 1][0] > elt:
                decal_col = 0
                size_col = len(M[0]) - 1
                mid_col = size_col // 2
                while decal_col <= size_col:
                    iteration += 1
                    if M[mid][mid_col] == elt:
                        return (mid, mid_col), iteration
                    elif M[mid][mid_col] > elt:
                        size_col = mid_col - 1
                    else:
                        decal_col = mid_col + 1
                    mid_col = (decal_col + size_col) // 2
                return None, iteration
            else:
                decal = mid + 1
        mid = (decal + size_line) // 2
    return None, iteration



def benchmark_matrice_dichoto(runs):
    relative_distance = list()
    itera_mat_glout = list()
    itera_mat_opti = list()
    for _ in progressbar.progressbar(range(runs)):
        line = random.randrange(4,16)
        col = random.randrange(5,14)
        matrice = generate_matrice_sorted(line, col)
        elt_i, elt_j = random.randrange(0,line), random.randrange(0,col)
        elt = matrice[elt_i][elt_j]
        value_greedy = find_elt_matrix_sort_glout(matrice, elt)[1]
        value_optimal = find_elt_matrix_sort_opti(matrice, elt)[1]
        itera_mat_glout.append(value_greedy)
        itera_mat_opti.append(value_optimal)
        relative_distance.append((value_greedy - value_optimal) / value_optimal)
    mean_greedy = np.mean(itera_mat_glout)
    mean_optimal = np.mean(itera_mat_opti)
    std_greedy = np.std(itera_mat_glout)
    std_optimal = np.std(itera_mat_opti)

    print(f"Greedy:\n\tmean:{mean_greedy}\n\tstd:{std_greedy}")
    print(f"Optimal:\n\tmean:{mean_optimal}\n\tstd:{std_optimal}")
    plt.hist(relative_distance, bins='auto')
    plt.show()

if __name__ == """__main__""":
    # mat = [[4, 8, 15, 19, 24, 27],
    #        [31, 35, 36, 40, 42, 43],
    #        [48, 53, 54, 60, 63, 70],
    #        [73, 76, 80, 81, 87, 94],
    #        [100, 105, 110, 111, 114, 116],
    #        [122, 129, 130, 137, 141, 145],
    #        [147, 152, 160, 173, 180, 193]]
    #
    # val = find_elt_matrix_sort_opti(mat, 35)
    # val2 = find_elt_matrix_sort_glout(mat, 35)
    # print(val)
    # print(val2)
    benchmark_matrice_dichoto(20000)
