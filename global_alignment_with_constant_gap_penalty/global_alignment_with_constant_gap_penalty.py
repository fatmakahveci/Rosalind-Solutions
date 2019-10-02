#!/bin/env/python

from Bio import SeqIO
from Bio.SubsMat.MatrixInfo import blosum62
from numpy import zeros
from itertools import product
from sys import setrecursionlimit


def blosum_score(seq1, seq2, i, j):
    cost = blosum62.get((seq1[i], seq2[j]))

    if cost == None:
        cost = blosum62.get((seq2[j], seq1[i]))
    return cost


def calculate_alignment_score(seq1, seq2, i, j, gap1, gap2, alignment_matrix):
    if (i < 0 and j >= 0) or (i >= 0 and j < 0):
        return gap_penalty
    elif i < 0 and j < 0:
        return 0
    elif alignment_matrix[i][j][gap1][gap2] != -1:
        return alignment_matrix[i][j][gap1][gap2]
    else:
        match = blosum_score(seq1, seq2, i - 1, j - 1) + calculate_alignment_score(seq1, seq2, i - 1, j - 1, 0, 0,
                                                                                   alignment_matrix)
    gap_seq1, gap_seq2 = 0, 0

    if gap1 == 0:
        gap_seq1 += gap_penalty
    gap_seq1 += calculate_alignment_score(seq1, seq2, i, j - 1, 1, 0, alignment_matrix)

    if gap2 == 0:
        gap_seq2 += gap_penalty
    gap_seq2 += calculate_alignment_score(seq1, seq2, i - 1, j, 0, 1, alignment_matrix)

    alignment_matrix[i][j][gap1][gap2] = max(match, gap_seq1, gap_seq2)
    return int(alignment_matrix[i][j][gap1][gap2])


def find_alignment_matrix(seq1, seq2, m, n):
    alignment_matrix = zeros((m + 1, n + 1, 2, 2))

    for i, j, k, l in product(range(m + 1), range(n + 1), range(2), range(2)):
        alignment_matrix[i][j][k][l] = -1

    return calculate_alignment_score(seq1, seq2, m - 1, n - 1, 0, 0, alignment_matrix)


if __name__ == '__main__':
    setrecursionlimit(10000)
    gap_penalty = -5

    seq1, seq2 = map(lambda x : str(x.seq), list(SeqIO.parse("rosalind.txt", 'fasta')))

    print(find_alignment_matrix(seq1, seq2, len(seq1), len(seq2)))
