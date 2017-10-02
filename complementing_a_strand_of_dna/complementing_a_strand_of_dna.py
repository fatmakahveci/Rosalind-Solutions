#!/bin/env/python

import sys


def main():
    seq = open('complementing_a_strand_of_dna.txt', 'r').read()
    seq_size = len(seq)
    for i in range(seq_size):
        nucl = seq[seq_size - i - 1]
        if nucl == 'A':
            sys.stdout.write('T')
        elif nucl == 'C':
            sys.stdout.write('G')
        elif nucl == 'G':
            sys.stdout.write('C')
        elif nucl == 'T':
            sys.stdout.write('A')
    print("")


if __name__ == "__main__":
    main()
