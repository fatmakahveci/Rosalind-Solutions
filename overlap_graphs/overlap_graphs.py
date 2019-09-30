#!/bin/env python3.7

import itertools

from Bio import SeqIO


if __name__ == "__main__":
    sequences = list(SeqIO.parse("rosalind.txt", 'fasta'))

    id_list = []
    seq_list = []

    for i in range(len(sequences)):
        id_list.append(sequences[i].id)
        seq_list.append(sequences[i].seq)

    for i, j in itertools.permutations(range(len(seq_list)), 2):
        if seq_list[i][-3:] == seq_list[j][:3]:
            print(id_list[i] + ' ' + id_list[j])
