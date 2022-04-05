import random
from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np
import progressbar


# 1) calcul de M[0:n+1][0:C+1] de terme gÃ©nÃ©ral M[k][c] = m(k,c)
def compute_M(V, E, C):
    n = len(V)
    M = [[c for c in range(0, C + 1)] for k in range(0, n + 1)]
    for c in range(C + 1): M[0][c] = 0  # base de la rÃ©currence
    # cas gÃ©nÃ©ral
    for k in range(1, n + 1):
        for c in range(C + 1):
            if E[k - 1] <= c:
                M[k][c] = max(V[k - 1] + M[k - 1][c - E[k - 1]], M[k - 1][c])
            else:  # le k-Ã¨me objet est trop encombrant pour le sac de contenance c
                M[k][c] = M[k - 1][c]
    return M


def get_max_bag_glout(M, V, E, k, c):
    bag = []
    weight = 0
    tuples_v_e = []
    for i in range(k):
        tuples_v_e.append((V[i], E[i]))
    tuples_v_e.sort(key=lambda y: y[0], reverse=True)
    for i in range(k):
        e = int(tuples_v_e[i][1])
        if (e + weight) <= c:
            weight += e
            #bag.append(([i, tuples_v_e[i][0], tuples_v_e[i][1]]))
            bag.append(tuples_v_e[i][0])
    return sum(bag)

def get_max_bag_opti(M, V, E, n, C):
    bag = []
    return sum(get_max_bag_opti_auxi(M, V, E, n, C, bag))


def get_max_bag_opti_auxi(M, V, E, k, c, bag):  # affichage du contenu du sac de contenance c, contenant un
    # sous-ensemble de [0:k], de valeur max.
    # appel principal : sac(M,n,C).
    if k == 0:
        bage = bag
        return bage
    if M[k][c] == M[k - 1][c]:  # le k-Ã¨me objet n'est pas dans le sac
        return get_max_bag_opti_auxi(M, V, E, k - 1, c, bag)  # l'affichage du sac "k,c" est obtenu en affichant le sac "k-1,c"
    else:
        #bag.append([k - 1, V[k - 1], E[k - 1]])
        bag.append(V[k - 1])
        return get_max_bag_opti_auxi(M, V, E, k - 1, c - E[k - 1], bag)  # afficher le sac "k-1,c-e(k-1)"
        #print(k - 1, end="\t")
        #print(V[k - 1], end="\t")
        #print(E[k - 1])  # afficher le k-Ã¨me objet



def main():
    # Exemples avec n = 10 objets
    #
    V = [6, 3, 9, 14, 12, 11, 3, 4, 9, 20]
    E = [2, 2, 6, 5, 4, 9, 6, 1, 1, 9]
    #
    for C in range(1, 11):
        print("V = ", V)
        print("E = ", E)
        M = compute_M(V, E, C)
        print("C = ", C)
        # pprint(M)
        print("Contenu du sac de valeur maximum : (numÃ©ro, valeur, encombrement)")
        n = len(V)
        test = get_max_bag_glout(M, V, E, n, C)
        print(test)
        print('---------------------------------------')


def benchmark_bag(runs):
    relative_distance = list()
    bag_glout = list()
    bag_opti = list()
    for _ in progressbar.progressbar(range(runs)):
        n = 50  # longueur des lites V et E
        C = random.randrange(100, 300)  # taille max de l'emcombrement
        V = []
        E = []
        for i in range(n):
            V.append(random.randrange(3, 20))
            E.append(random.randrange(3, 20))
        M = compute_M(V, E, C)
        value_optimal = get_max_bag_opti(M, V, E, n, C)
        value_greedy = get_max_bag_glout(M, V, E, n, C)
        bag_glout.append(value_greedy)
        bag_opti.append(value_optimal)
        relative_distance.append((value_greedy - value_optimal) / value_optimal)
    mean_greedy = np.mean(bag_glout)
    mean_optimal = np.mean(bag_opti)
    std_greedy = np.std(bag_glout)
    std_optimal = np.std(bag_opti)

    print(f"Greedy:\n\tmean:{mean_greedy}\n\tstd:{std_greedy}")
    print(f"Optimal:\n\tmean:{mean_optimal}\n\tstd:{std_optimal}")
    plt.hist(relative_distance, bins='auto')
    plt.show()


if __name__ == """__main__""":
    benchmark_bag(20000)
