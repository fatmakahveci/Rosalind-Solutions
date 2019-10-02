#!/usr/bin/env python3.7

from itertools import product
from Bio import SeqIO


if __name__ == "__main__":
    seq = str(list(SeqIO.parse("rosalind.txt","fasta"))[0].seq)
    kmers = {}

    for kmer in [''.join(x) for x in product('ATGC', repeat=4)]:
        kmers[kmer] = 0

    for i in range(len(seq) - (4 - 1)):
        kmer = seq[i:i + 4]
        kmers[kmer] += 1

    result = []
    for kmer in sorted(kmers.iterkeys()):
        result.append(kmers[kmer])

    print(' '.join(map(str,result)))
