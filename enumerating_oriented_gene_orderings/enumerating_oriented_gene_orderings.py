#!/bin/env/python

import itertools


def main():
    n = int(open('enumerating_oriented_gene_orderings.txt', 'r').read())
    
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


if __name__ == '__main__':
    main()

