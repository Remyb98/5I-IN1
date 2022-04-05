import random
from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np
import progressbar


def calculerMA(G):  # G[0:n+1]][0:S+1] est de terme général G[i][s] = g(i,s) = gain obtenu
    # par la livraison d'un stock s à l'entrepôt de numéro i.
    n = len(G)
    S = len(G[0]) - 1
    M = [[-1 for s in range(S + 1)] for k in range(n + 1)]  # -1, ou une valeur quelconque.
    A = [[0 for s in range(S + 1)] for k in range(n + 1)]  # 0 ou une valeur quelconque.
    # base de la récurrence : m
    for s in range(S + 1): M[0][s] = 0  # m(0,s) = 0 qqsoit s, 0 ? s < S+1
    # cas général : par taille k croissante, calculer et mémoriser toutes les valeurs m(k,s)
    # qqsoit k, qqsoit s, 1 ? k < n+1, 0 ? s < S+1
    # m(k,s) =  max_{0 ?  s' < s+1} ( g(k-1,s') + m(k-1,s-s') )
    for k in range(1, n + 1):  # par tailles k croissantes
        for s in range(0, S + 1):  # pour tout stock s
            # calculer m(k,s) = max_{0 ?  s' < s+1} ( g(k-1,s') + m(k-1,s-s') )
            for sprime in range(0, s + 1):
                mks = G[k - 1][sprime] + M[k - 1][s - sprime]
                if mks > M[k][s]:
                    M[k][s] = mks
                    A[k][s] = sprime
    #return M, A*
    return M[n][s]


# complexité Theta(n x S^2)

def affichageRO(A, G, k, s):  # affichage d'une répartition optimale (RO) du stock s sur
    # le sous-ensemble des k premiers entrepôts
    # Appel principal : affichageRO(A,G,n,S)
    if k == 0: return  # sans rien faire, la RO du stock s sur [0:0] = Ø est affichée.
    # k > 0
    sk = A[k][s]  # qté livrée au k-ème entrepôt dans la RO du stock s sur [0:k]
    affichageRO(A, G, k - 1, s - sk)  # la RO du stock s-sk sur [0:k-1] a été affichée
    print("sk = ", sk)

    # affichage du gain g(k-1,sk) obtenu en livrant sk au k-ème entrepôt
    print("g(" + str(k - 1) + "," + str(sk) + ") = " + str(G[k - 1][sk]))


def stock_glouton(G, k, S):
    indices = [0] * len(G)
    all_gain = 0
    for _ in range(S):
        gain = 0
        indice = 0
        for line in range(k):
            val = G[line][indices[line]]
            val2 = G[line][indices[line] + 1]
            if val2 - val > gain:
                gain = val2 - val
                indice = line
        all_gain += gain
        indices[indice] += 1
    return all_gain


def benchmark_stock(runs):
    relative_distance = list()
    max_stocks_glout = list()
    max_stocks_opti = list()
    for _ in progressbar.progressbar(range(runs)):
        G = []
        N = random.randrange(4, 8)
        S = random.randrange(8, 12)
        for i in range(N):
            s = [0]
            for j in range(S - 1):
                val = random.randint(1, 7)
                while val <= s[j]:
                    val = random.randint(s[j], 7 + s[j])
                s.append(val)
            G.append(s)

        value_greedy = stock_glouton(G, N, S-1)
        value_optimal = calculerMA(G)
        max_stocks_glout.append(value_greedy)
        max_stocks_opti.append(value_optimal)
        relative_distance.append((value_greedy - value_optimal) / value_optimal)
    mean_greedy = np.mean(max_stocks_glout)
    mean_optimal = np.mean(max_stocks_opti)
    std_greedy = np.std(max_stocks_glout)
    std_optimal = np.std(max_stocks_opti)

    print(f"Greedy:\n\tmean:{mean_greedy}\n\tstd:{std_greedy}")
    print(f"Optimal:\n\tmean:{mean_optimal}\n\tstd:{std_optimal}")
    plt.hist(relative_distance, bins='auto')
    plt.show()


if __name__ == """__main__""":
    benchmark_stock(20000)