#!/bin/env/python

import itertools
import sys


def read_file(file_name):
    return open(file_name, 'r').read()


def main():
    file_content = read_file("enumerating_k_mers_lexicographically.txt").split('\n')

    alphabet = str(file_content[0]).replace('[', '').replace(']', '').split(' ')
    alphabet.sort()
    k = int(file_content[1])
    dna_collection = list(itertools.product(alphabet, repeat=k))

    for element in dna_collection:
        for i in range(k):
            sys.stdout.write(element[i])
        print('')


if __name__ == "__main__":
    main()
