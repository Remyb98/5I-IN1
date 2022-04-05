import random
from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np
import progressbar


def niveau(i):
    l = 0
    while not i in range((l - 1) * l // 2, l * (l + 1) // 2):
        l = l + 1
    return l - 1


def g(i):
    l = niveau(i)
    p = i - l * (l + 1) // 2  # position de i dans l'intervalle [l*(l+1)/2 : (l+1)*(l+2)/2]
    # l'indice g(i) est à la même position dans l'intervalle [(l+1)*(l+2)/2 : (l+2)*(l+3)/2]
    return (l + 1) * (l + 2) // 2 + p


def feuille(i, n):
    return g(i) >= n


def generate_random_triangle(level, rand_rang):
    liste = []
    for _ in range((level * (level + 1)) // 2):
        liste.append(random.randint(1, rand_rang))
    return liste


def d(i):
    return g(i)+1


def get_max_path_glout(triangle):
    max = 0
    i = 0
    while 1:
        max += triangle[i]
        if feuille(i, len(triangle)):
            break
        if triangle[g(i)] > triangle[d(i)]:
            i = g(i)
        else:
            i = d(i)
    return max


def get_max_path_opti(triangle):
    return get_max_path_opti_auxi(triangle, 0)


def get_max_path_opti_auxi(triangle, i):
    if feuille(i, len(triangle)):
        return triangle[i]

    left_val = get_max_path_opti_auxi(triangle, g(i))
    right_val = get_max_path_opti_auxi(triangle, d(i))
    return triangle[i] + max(left_val, right_val)

def benchmark_triangle(runs):
    relative_distance = list()
    max_triangle_glout = list()
    max_triangle_opti = list()
    for _ in progressbar.progressbar(range(runs)):
        level = random.randrange(10,17)
        triangle = generate_random_triangle(level, 20)
        value_greedy = get_max_path_glout(triangle)
        value_optimal = get_max_path_opti(triangle)
        max_triangle_glout.append(value_greedy)
        max_triangle_opti.append(value_optimal)
        relative_distance.append((value_greedy - value_optimal) / value_optimal)
    mean_greedy = np.mean(max_triangle_glout)
    mean_optimal = np.mean(max_triangle_opti)
    std_greedy = np.std(max_triangle_glout)
    std_optimal = np.std(max_triangle_opti)

    print(f"Greedy:\n\tmean:{mean_greedy}\n\tstd:{std_greedy}")
    print(f"Optimal:\n\tmean:{mean_optimal}\n\tstd:{std_optimal}")
    plt.hist(relative_distance, bins='auto')
    plt.show()


if __name__ == """__main__""":
    # level = 10
    # rand = 20
    # #triangle = generate_random_triangle(level,rand)
    # triangle = [1,2,3,5,1,2,25,1,3,1]
    # val = get_max_path_glout(triangle)
    # val2 = get_max_path_opti(triangle)
    # print(val)
    # print(val2)
    benchmark_triangle(20000)