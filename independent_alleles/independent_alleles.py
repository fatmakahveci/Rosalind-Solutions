#!/bin/env/python

import math


def read_file(file_name):
    return open(file_name, 'r').read()


def get_variables(file_name):
    return map(int, read_file(file_name).split(' '))


def independent_alleles(file_name):
    variables = get_variables(file_name)
    k = variables[0]
    N = variables[1]
    
    sum = 0
    
    for i in range(N, int(math.pow(2, k) + 1)):
        sum += (math.factorial(math.pow(2, k)) / (
                                                  (math.factorial(math.pow(2, k) - i)) * (math.factorial(i)))) * math.pow(0.25, i) * math.pow(0.75,
                                                                                                                                              math.pow(2, k) - i)
    print(sum)


def main():
    independent_alleles('independent_alleles.txt')


if __name__ == '__main__':
    main()

