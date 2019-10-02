#!/usr/bin/env python3.7

import itertools


if __name__ == "__main__":
    with open("rosalind.txt", 'r') as file:
        n = int(file.readline().strip('\n'))
        file.close()

    permutations = []
    nr = 0
    whole_list = itertools.permutations(list(range(1, n + 1)))

    for i in whole_list:
        sign_list = itertools.product([-1, 1], repeat=n)
        for j in sign_list:
            permutation = [a * sign for a, sign in zip(i, j)]
            permutations.append(permutation)
            nr += 1
    print(nr)

    for i in range(nr):
        print(' '.join(map(str, permutations[i])))
