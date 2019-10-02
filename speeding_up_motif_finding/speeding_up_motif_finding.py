#!/usr/bin/env python3.7

from Bio import SeqIO


if __name__ == '__main__':
    pattern = str(list(SeqIO.parse("rosalind.txt", 'fasta'))[0].seq)
    m = len(pattern)
    failure = [0] * m
    i, j = 1, 0

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
    print(' '.join(map(str, failure)))
