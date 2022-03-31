import random
import matplotlib.pyplot as plt
import numpy as np
import progressbar

# [N, E, NE]
weight = list(range(3))

def N(x, y, m):
    if x == m-1:
        return float("inf")
    return weight[0]


def E(x, y, n):
    if y == n-1:
        return float("inf")
    return weight[1]


def NE(x, y, m, n):
    if x == m - 1 or y == n - 1:
        return float("inf")
    return weight[2]


def compute_M(m, n):
    """O(m x n)"""
    M = [[float("inf") for c in range(n)] for l in range(m)]

    M[0][0] = 0
    for x in range(1, m):
        M[x][0] = M[x - 1][0] + N(x - 1, 0, m)
    for y in range(1,n):
        M[0][y] = M[0][y - 1] + E(0, y - 1, n)

    for x in range(1,m):
        for y in range(1,n):
            M[x][y] = min(
                N(x - 1, y, m) + M[x - 1][y],
                E(x, y - 1, n) + M[x][y - 1],
                NE(x - 1, y - 1, m, n) + M[x - 1][y - 1]
            )
    return M


def accm(x,y,M,m,n):
    if (x, y) == (0, 0):
        return 0
    if y == 0:
        return N(x - 1, 0, m) + accm(x - 1, 0, M, m, n)
    if x == 0:
        return accm(0, y - 1, M, m, n) + E(0, y - 1, n)

    cminN = N(x - 1, y, m) + M[x - 1][y]
    cminE = E(x, y - 1, n) + M[x][y - 1]
    cminNE = NE(x - 1, y - 1,m, n) + M[x - 1][y - 1]

    if cminN <= min(cminE, cminNE):
        return accm(x - 1, y, M, m, n) + N(x - 1, y, m)
    elif cminE <= cminNE:
        return accm(x, y - 1, M, m, n) + E(x, y - 1, n)
    else:
        return accm(x - 1, y - 1, M, m, n) + NE(x - 1, y - 1, m, n)


def glouton_robot(x, y, M, m, n):
    if (x, y) == (0, 0):
        return 0
    if y == 0:
        return N(x - 1, 0, m) + glouton_robot(x - 1, 0, M, m, n)
    if x == 0:
        return glouton_robot(0, y - 1, M, m, n) + E(0, y - 1, n)

    cminN = N(x - 1, y, m)
    cminE = E(x, y - 1, n)
    cminNE = NE(x - 1, y - 1, m, n)
    if cminN <= min(cminE, cminNE):
        return glouton_robot(x - 1, y, M, m, n) + cminN
    if cminE <= cminNE:
        return glouton_robot(x, y - 1, M, m, n) + cminE
    return glouton_robot(x - 1, y - 1, M, m, n) + cminNE


def afficher(M):
    m, n = len(M), len(M[0])
    for x in range(m-1, -1, -1):
        line = ""
        for y in range(n):
            line += f"{M[x][y]},\t"
        print(line[:-2])


def benchmark_robot(runs):
    relative_distance = list()
    values_optimal = list()
    values_greedy = list()

    for _ in progressbar.progressbar(range(runs)):
        m, n = random.randint(10, 100), random.randint(10, 100)
        for j in range(2):
            weight[j] = random.randint(1, 4)
        M = compute_M(m,  n)
        value_optimal = accm(m - 1, n - 1, M, m, n)
        value_greedy = glouton_robot(m - 1, n - 1, M, m, n)

        values_optimal.append(value_optimal)
        values_greedy.append(value_greedy)
        relative_distance.append((value_greedy - value_optimal) / value_optimal)
    mean_greedy = np.mean(values_greedy)
    mean_optimal = np.mean(value_optimal)
    std_greedy = np.std(values_greedy)
    std_optimal = np.std(values_optimal)

    print(f"Greedy:\n\tmean:{mean_greedy}\n\tstd:{std_greedy}")
    print(f"Optimal:\n\tmean:{mean_optimal}\n\tstd:{std_optimal}")
    plt.hist(relative_distance, bins='auto')
    plt.show()


if __name__ == '__main__':
    benchmark_robot(10)
