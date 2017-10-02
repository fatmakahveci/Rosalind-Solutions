#!/bin/env/python

import sys

variables = open('finding_a_motif_in_dna.txt', 'r').read().split('\n')

s = str(variables[0])
t = str(variables[1])


def main():
    i = 0
    for i in range(len(s)):
        for j in range(len(t)):
            if s[i:i + len(t)] == t[:]:
                sys.stdout.write(str(i + 1) + ' ')
                break
    print('')


if __name__ == '__main__':
    main()

