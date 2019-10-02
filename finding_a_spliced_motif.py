#!/usr/bin/env python3.7

from Bio import SeqIO

if __name__ == '__main__':
    s, t = map(lambda x: str(x.seq), list(SeqIO.parse("rosalind.txt","fasta")))

    idx_list = []
    i, j = 0, 0
    while i < len(s) and j < len(t):
        if s[i] == t[j]:
            idx_list.append(str(i+1))
            j += 1
        i += 1
    print(' '.join(idx_list))
