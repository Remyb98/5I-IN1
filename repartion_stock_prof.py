# -*- coding: latin-1 -*-

# 18/01/2022 rene.natowicz@esiee.fr
# feuille 1 exercice 3. R�partition optimale d'un stock sur un ensemble de n entrep�ts.
"""
Notation : m(n,S) = gain total maximum d'une r�partition du stock S sur le sous-ensemble
[0:n] des n entrep�ts.

Probl�me de taille n-1 : seuls les entrep�ts [0:n-1] sont livr�s
Probl�me de taille n : seuls les entrep�ts [0:n] sont livr�s
Seule diff�rence entre les deux : on autorise la livraison du n-�me entrep�t. 

1) Supposons le probl�me r�solu?
Quelle a �t� la derni�re �tape de r�solution ? 
On a autoris� la livraison du n-�me entrep�t.

Qu'a-t-il pu se passer ? 
On a pu lui livrer 0 (rien n'a livr�), ou 1, ou 2, ... ou S (la totalit� du stock).

Si on livre 0 au n-�me entrep�t, il reste un stock S � r�partir sur le sous-ensemble 
d'entrep�ts [0:n-1]. On a m(n,S) = g(n-1,0) + m(n-1,S) = 0 + m(n-1,S) = m(n-1,S). 
Remarque : la r�partition de S sur [0:n-1] est de gain total maximum (c'est-�-dire
de valeur m(n-1,S).) 
Imaginons que �a ne soit pas le cas. Soit m'(n-1,S) < m(n-1,S) sa valeur. 
Alors m(n,S) = m'(n-1,S) n'est pas maximum puisque m'(n-1,S) n'est pas maximum.
Or, par hypoth�se, m(n,S) est maximum. Donc, la r�partition de S sur [0:n-1]
est n�cessairement maximum, donc de gain total m(n-1,S). 

Si on livre 1, au n-�me entrep�t (de num�ro n-1) le gain obtenu par cette livraison 
est g(n-1,1). Il reste un stock S-1 � r�partir sur le sous-ensemble [0:n-1] des 
n-1 premiers entrep�ts. Cette r�partition doit �tre de gain total maximum, m(n-1,S-1)
(sinon la r�partition du stock S sur les n entrep�ts ne serait pas maximum, ce qui 
serait absurde puisque par hypoth�se m(n,S) est maximum.)
Ainsi : si on livre 1 au n-�me entrep�t, m(n,S) = g(n-1,1) + m(n-1,S-1)

Si on livre 2 au n-�me entrep�t, m(n,S) = g(n-1,2) + m(n-1,S-2).
etc.
Si on livre S au n-�me entrep�t, m(n,S) = g(n-1,S) + m(n-1,0).

De fa�on g�n�rale, si on livre un stock s' au n-�me entrep�t, il reste un stock
S-s', � r�partir avec un gain maximum sur le sous-ensemble des n-1 premiers 
entrep�ts et la r�partition optimale aura la valeur m(n,S) = g(n-1,s') + m(n-1,S-s').

Remarque/Rappel : dans l'�criture " g(n-1,s') ", le premier argument, "n-1", est 
le num�ro du n-�me entrep�t, alors que dans " m(n-1,S-s') ", ce premier argument "n-1" 
d�signe le sous-ensemble n-1 premiers entrep�ts.

Soit m(n,S) le gain total max. d'une r�partition du stock S sur le sous-ensemble
des n premiers entrep�ts, c'est-�-dire sur l'ensemble des entrep�ts.

m(n,S) = Max{
			g(n-1,s'=0) + m(n-1,S-0), <<< 0 livr� au n-�me entrep�t
			g(n-1,s'=1) + m(n-1,S-1), <<< 1 
			g(n-1,s'=2) + m(n-1,S-2), <<< 2
			...
			g(n-1,s') + m(n-1,S-s')   <<< s' livr� au n-�me entrep�t
			...
			g(n-1,s'=S) + m(n-1,S-S=0) <<< S livr� au n-�me entrep�t
		}

Pour faire court : m(n,S) = Max_{0 ?  s' < S+1} ( g(n-1,s') + m(n-1,S-s') )

2) G�n�ralisation de cette expression 
	m(k,s) =  gain total max d?une r�partition d?un stock s sur le sous-ensemble 
	des k premiers entrep�ts. 

    qqsoit k, 1 ? k < n+1, qqsoit s, 0 ? s < S+1 : 
    m(k,s) =  max_{0 ?  s' < s+1} ( g(k-1,s') + m(k-1,s-s') )


3) Cas de base : m(0, s) = valeur maximum de la r�partition du stock s sur 
le sous-ensemble des 0 premiers entrep�ts, c'est-�-dire sur l'ensemble vide. 
Aucun entrep�t n'est livr�, nous avons donc :
	qqsoit s, 0 ? s < S+1
    m(0, s) = g(0,0) + g(1,0) + ... + g(n-1,0) = 0 + 0 + ... 0 = 0, 
????????????
On calculera un tableau M[0:n+1][0:S+1] de terme g�n�ral M[k][s] = m(k,s)
ET un tableau A[0:n+1][0:S+1] de terme g�n�ral A[k][s] = a(k,s) = argmax m(k,s) = 
quantit� livr�e au k-�me entrep�t dans la r�partition optimale du stock s sur 
le sous-ensemble des k premiers entrep�ts. 
Voir ci-dessous la fonction calculerMA(G) qui calcule et retourne les deux tableaux 
M et A. 

Les valeurs a(k,s) permettent de construire la solution c'est-�-dire permettent
d'afficher une r�partition optimale du stock s sur le sous-ensemble [0:k] 
des k premiers entrep�ts (fonction afficherRO(...,k,s)). L'appel principal
afficherRO(...,n,S) affichera une r�partition optimale du stock S sur le sous-ensemble
[0:n] des n entrep�ts, c'est-�-dire sur l'ensemble des n entrep�ts.

"""
from pprint import pprint

G = [
    [0, 2, 4, 6, 8, 9, 9],
    [0, 1, 2, 3, 4, 5, 6],
    [0, 2, 4, 5, 6, 6, 6],
    [0, 3, 4, 4, 5, 5, 5]]

S = 6
n = 4

all_gain = 0
for col in range(S - 1):
    gain = 0
    for line in range(n):
        test = G[line][col]
        test2 = G[line][col + 1]
        if G[line][col + 1] - G[line][col] > gain:
            gain = G[line][col + 1] - G[line][col]
    all_gain += gain


def calculerMA(G):  # G[0:n+1]][0:S+1] est de terme g�n�ral G[i][s] = g(i,s) = gain obtenu
    # par la livraison d'un stock s � l'entrep�t de num�ro i.
    n = len(G)
    S = len(G[0]) - 1
    M = [[-1 for s in range(S + 1)] for k in range(n + 1)]  # -1, ou une valeur quelconque.
    A = [[0 for s in range(S + 1)] for k in range(n + 1)]  # 0 ou une valeur quelconque.
    # base de la r�currence : m
    for s in range(S + 1): M[0][s] = 0  # m(0,s) = 0 qqsoit s, 0 ? s < S+1
    # cas g�n�ral : par taille k croissante, calculer et m�moriser toutes les valeurs m(k,s)
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
    return M, A


# complexit� Theta(n x S^2)

def affichageRO(A, G, k, s):  # affichage d'une r�partition optimale (RO) du stock s sur
    # le sous-ensemble des k premiers entrep�ts
    # Appel principal : affichageRO(A,G,n,S)
    if k == 0: return  # sans rien faire, la RO du stock s sur [0:0] = � est affich�e.
    # k > 0
    sk = A[k][s]  # qt� livr�e au k-�me entrep�t dans la RO du stock s sur [0:k]
    affichageRO(A, G, k - 1, s - sk)  # la RO du stock s-sk sur [0:k-1] a �t� affich�e
    print("sk = ", sk)

    # affichage du gain g(k-1,sk) obtenu en livrant sk au k-�me entrep�t
    print("g(" + str(k - 1) + "," + str(sk) + ") = " + str(G[k - 1][sk]))


def main():
    # G[0:n][0:S+1] de terme g�n�ral G[i][s] = g(i,s)
    G = [  # n = 4 entrep�ts (4 lignes) et stock S = 6 (7 colonnes)
        [0, 2, 4, 6, 8, 9, 9],
        [0, 1, 2, 3, 4, 5, 6],
        [0, 2, 4, 5, 6, 6, 6],
        [0, 3, 4, 4, 5, 5, 5]
    ]
    print("G = ")
    pprint(G)
    print("MA = ")
    MA = calculerMA(G)
    pprint(MA)
    A = MA[1]  # A[0:n+1][0:S+1] de terme g�n�ral a(k,s) = argmax m(k,s)

    n = len(A) - 1
    S = len(G[0]) - 1
    print("A = ")
    pprint(A)
    print("S = ", S)
    print("n = ", n)
    affichageRO(A, G, n, S)
    print("----------")
    M = MA[0]
    print("m(n,S) = " + str(M[n][S]))
    print()
    #
    # # G[0:n][0:S+1] de terme g�n�ral G[i][s] = g(i,s)
    # G = [  # n = 4 entrep�ts (4 lignes) et stock S = 6 (7 colonnes)
    #     [0, 1, 2, 2, 2, 2, 2],
    #     [0, 1, 2, 3, 3, 3, 3],
    #     [0, 1, 2, 3, 4, 4, 4],
    #     [0, 1, 2, 3, 4, 5, 6]
    # ]
    # print("G = ", G)
    # MA = calculerMA(G)
    # A = MA[1]  # A[0:n+1][0:S+1] de terme g�n�ral a(k,s) = argmax m(k,s)
    # n = len(A) - 1
    # S = len(G[0]) - 1
    # affichageRO(A, G, n, S)
    # print("----------")
    # M = MA[0]
    # print("m(n,S) = " + str(M[n][S]))
    # print()
    #
    # # G[0:n][0:S+1] de terme g�n�ral G[i][s] = g(i,s)
    # G = [  # n = 4 entrep�ts (4 lignes) et stock S = 6 (7 colonnes)
    #     [0, 1, 1, 1, 1, 1, 1],
    #     [0, 1, 1, 1, 1, 1, 2],
    #     [0, 1, 1, 1, 1, 1, 3],
    #     [0, 1, 1, 1, 1, 1, 4],
    # ]
    # MA = calculerMA(G)
    # A = MA[1]  # A[0:n+1][0:S+1] de terme g�n�ral a(k,s) = argmax m(k,s)
    # n = len(A) - 1
    # S = len(G[0]) - 1
    # affichageRO(A, G, n, S)
    # print("----------")
    # M = MA[0]
    # print("m(n,S) = " + str(M[n][S]))
    # print()
    #
    # # G[0:n][0:S+1] de terme g�n�ral G[i][s] = g(i,s)
    # G = [  # n = 4 entrep�ts (4 lignes) et stock S = 6 (7 colonnes)
    #     [0, 1, 1, 1, 1, 1, 1],
    #     [0, 1, 1, 1, 1, 1, 2],
    #     [0, 1, 1, 1, 1, 1, 3],
    #     [0, 1, 1, 1, 1, 1, 5], ]
    # MA = calculerMA(G)
    # A = MA[1]  # A[0:n+1][0:S+1] de terme g�n�ral a(k,s) = argmax m(k,s)
    # n = len(A) - 1
    # S = len(G[0]) - 1
    # affichageRO(A, G, n, S)
    # print("----------")
    # M = MA[0]
    # print("m(n,S) = " + str(M[n][S]))
    # print()
    #
    # # G[0:n][0:S+1] de terme g�n�ral G[i][s] = g(i,s)
    # G = [  # n = 4 entrep�ts (4 lignes) et stock S = 6 (7 colonnes)
    #     [0, 1, 2, 2, 2, 2, 2],
    #     [0, 1, 1, 3, 3, 3, 3],
    #     [0, 1, 1, 1, 4, 4, 4],
    #     [0, 1, 1, 1, 1, 1, 5],
    # ]
    # MA = calculerMA(G)
    # A = MA[1]  # A[0:n+1][0:S+1] de terme g�n�ral a(k,s) = argmax m(k,s)
    # n = len(A) - 1
    # S = len(G[0]) - 1
    # affichageRO(A, G, n, S)
    # print("----------")
    # M = MA[0]
    # print("m(n,S) = " + str(M[n][S]))
    # print()


""" Trace de l'ex�cution du programme dans un terminal Unix.

% python

WARNING: Python 2.7 is not recommended. 
This version is included in macOS for compatibility with legacy software. 
Future versions of macOS will not include Python 2.7. 
Instead, it is recommended that you transition to using 'python3' from within Terminal.

Python 2.7.16 (default, Aug 30 2021, 14:43:11) 
[GCC Apple LLVM 12.0.5 (clang-1205.0.19.59.6) [+internal-os, ptrauth-isa=deploy on darwin
Type "help", "copyright", "credits" or "license" for more information.

>>> import feuille1_exercice3_2022; reload(feuille1_exercice3_2022); from feuille1_exercice3_2022 import *
<module 'feuille1_exercice3_2022' from 'feuille1_exercice3_2022.pyc'>
>>> import feuille1_exercice3_2022; reload(feuille1_exercice3_2022); from feuille1_exercice3_2022 import *
<module 'feuille1_exercice3_2022' from 'feuille1_exercice3_2022.py'>
>>> main()
G =  [[0, 2, 4, 6, 8, 9, 9], [0, 1, 2, 3, 4, 5, 6], [0, 2, 4, 5, 6, 6, 6], [0, 3, 4, 4, 5, 5, 5]]
g(0,4) = 8
g(1,0) = 0
g(2,1) = 2
g(3,1) = 3
----------
m(n,S) = 13

G =  [[0, 1, 2, 2, 2, 2, 2], [0, 1, 2, 3, 3, 3, 3], [0, 1, 2, 3, 4, 4, 4], [0, 1, 2, 3, 4, 5, 6]]
g(0,2) = 2
g(1,3) = 3
g(2,1) = 1
g(3,0) = 0
----------
m(n,S) = 6

g(0,1) = 1
g(1,1) = 1
g(2,1) = 1
g(3,1) = 1
----------
m(n,S) = 4

g(0,0) = 0
g(1,0) = 0
g(2,0) = 0
g(3,6) = 5
----------
m(n,S) = 5

g(0,2) = 2
g(1,3) = 3
g(2,1) = 1
g(3,0) = 0
----------
m(n,S) = 6

>>> 

"""

if __name__ == """__main__""":
    main()
