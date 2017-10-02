#!/bin/env/python

from Bio import SeqIO
from io import StringIO

file_name = 'speeding_up_motif_finding.txt'


def failure_function(pattern):
    m = len(pattern)
    failure = [0] * m
    i = 1
    j = 0

    while i < m:
        if pattern[i] == pattern[j]:
            failure[i] = j + 1
            i += 1
            j += 1
        elif j > 0:
            j = failure[j - 1]
        else:
            failure[i] = 0
            i += 1
    return failure


def main():
    pattern = list(SeqIO.parse(StringIO(open(file_name, 'r').read()), 'fasta'))[0].seq
    print(failure_function(pattern))


if __name__ == '__main__':
    main()
