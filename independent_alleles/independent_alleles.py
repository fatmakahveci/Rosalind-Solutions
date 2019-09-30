#!/bin/env/python3.7

import math


if __name__ == '__main__':
    k, N = map(int, open("rosalind.txt", 'r').read().split(' '))
    
    sum = 0
    
    for i in range(N, 2**k + 1):
        sum += (math.factorial(2**k) / ((math.factorial(2**k - i)) * (math.factorial(i)))) * 0.25**i * 0.75**(2**k - i)

    print("%.3f"%sum)
