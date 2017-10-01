#!/bin/env/python

import math

file_name='partial_permutations.txt'

def main():
    n=int(open(file_name,'r').read().split(' ')[0])
    k=int(open(file_name,'r').read().split(' ')[1])

    permutation=1
    for i in range(k):
        permutation *= (n - i)
    print(permutation%1000000)

if __name__ == "__main__":
    main()