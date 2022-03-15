import matplotlib.pyplot as plt
import numpy as np
import random

# [N, E, NE]
weight = list(range(3))

def N(x,y,m) :
    if x == m-1 : return float("inf") 
    return weight[0]


def E(x,y,n) :
    if y == n-1 : return float("inf")
    return weight[1]


def NE(x,y,m,n) :
    if x == m-1 or y == n-1 : return float("inf")
    return weight[2]


def calculerM(m,n) :
    M = [[float("inf") for c in range(n)] for l in range(m)]
    # base de la récurrence
    M[0][0] = 0
    for x in range(1, m):
    	M[x][0] = M[x-1][0] + N(x-1,0,m)
    for y in range(1,n):
    	M[0][y] = M[0][y-1] + E(0,y-1,n)
    # cas général : 1 ≤ x < m, 1 ≤ y < n
    for x in range(1,m) : 
        for y in range(1,n) :
            M[x][y] = min(
                N(x-1,y,m) + M[x-1][y], 
                E(x,y-1,n) + M[x][y-1],
                NE(x-1,y-1,m,n) + M[x-1][y-1] 
            )
    return M
    # complexité en Theta(m x n)


def accm(x,y,M,m,n) :
    if (x,y) == (0,0) : 
        return 0
    if y == 0 :
        return N(x-1,0,m) + accm(x-1,0,M,m,n) 
    if x == 0 :
        return accm(0,y-1,M,m,n) + E(0,y-1,n)

    # cas général : 1 ≤ x < m, 1 ≤ y < n
    cminN = N(x-1,y,m) + M[x-1][y] # coût min si dernier mvt N. 
    cminE = E(x,y-1,n) + M[x][y-1] # coût min si dernier mvt E. 
    cminNE = NE(x-1,y-1,m,n) + M[x-1][y-1] # coût min si dernier mvt NE.

    if cminN <= min(cminE,cminNE) : # le dernier mvt a été N
        return accm(x-1,y,M,m,n) + N(x-1,y,m)
    elif cminE <= cminNE : # le dernier mvt a été E
        return accm(x,y-1,M,m,n) + E(x,y-1,n)
    else : # le dernier mvt a été NE
        return accm(x-1,y-1,M,m,n) + NE(x-1,y-1,m,n)


def glouton_robot(x, y, M, m, n):
    if((x,y) == (0,0)):
        return 0
    if y == 0 :
        return N(x-1,0,m) + glouton_robot(x-1,0,M,m,n) # le ccm de (0,0) à (x-1,0) est affiché
    if x == 0 :
        return glouton_robot(0,y-1,M,m,n) + E(0,y-1,n)
    # cas général : 1 ≤ x < m, 1 ≤ y < n
    cminN = N(x-1,y,m) 
    cminE = E(x,y-1,n)
    cminNE = NE(x-1,y-1,m,n)
    if cminN <= min(cminE,cminNE) : # le dernier mvt a été N
        return glouton_robot(x-1,y,M,m,n) + cminN
    elif cminE <= cminNE : # le dernier mvt a été E
        return glouton_robot(x,y-1,M,m,n) + cminE # le ccm de (0,0) à (x,y-1) a été affiché.
    else : # le dernier mvt a été NE
        return glouton_robot(x-1,y-1,M,m,n) + cminNE# le ccm de (0,0) à (x-1,y-1) a été affiché.


def afficher(M) :
    m,n = len(M),len(M[0])
    for x in range(m-1,-1,-1) :
        line = ""
        for y in range(n) : 
            line += str(M[x][y]) + ",\t"
        print(line[:-2])


def main() :
    N = 1000
    distance_relative = list()
    values_optimal = list()
    values_greedy = list()

    for i in range (N):
        #Une matrice variante de taille (2,2) à (10,10)
        m = random.randrange(2, 10)
        n = random.randrange(2, 10)
        for j in range(2):
            weight[j] = random.randrange(1, 3) #On change les poids des directions entre 1 et 3
        
        M = calculerM(m, n)
        optimal = accm(m-1,n-1,M,m,n)
        glouton = glouton_robot(m-1,n-1,M,m,n)
        values_optimal.append(optimal)
        values_greedy.append(glouton)
        distance_relative.append((glouton - optimal) / optimal)

    num_bins = N // 2
    mean_greedy = np.mean(glouton)
    std_greedy = np.std(glouton)

    mean_optimal = np.mean(optimal)
    std_optimal = np.std(optimal)

    print(f"Greedy :\n\tmean:{mean_greedy}\n\tstd:{std_greedy}")
    print(f"Optimal :\n\tmean:{mean_optimal}\n\tstd:{std_optimal}")
    plt.hist(distance_relative, num_bins)
    plt.show()


if __name__ == '__main__':
	main()
