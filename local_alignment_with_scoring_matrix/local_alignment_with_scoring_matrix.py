#!/bin/env/python

from Bio import SeqIO
from Bio.SubsMat.MatrixInfo import pam250
from itertools import product
from numpy import zeros, where

file_name = 'local_alignment_with_scoring_matrix.txt'


def find_alignment_matrix():
    m, n = len(seq1), len(seq2)

    alignment_matrix = zeros((m + 1, n + 1))
    path_matrix = zeros((m + 1, n + 1))

    for i in range(0, m + 1):
        alignment_matrix[i][0] = i * (-gap_penalty)
        path_matrix[i][0] = 4

    for j in range(0, n + 1):
        alignment_matrix[0][j] = j * (-gap_penalty)
        path_matrix[0][j] = 4

    for i, j in product(range(1, m + 1), range(1, n + 1)):
        cost = pam250.get((seq1[i - 1], seq2[j - 1]))
        if cost == None:
            cost = pam250.get((seq2[j - 1], seq1[i - 1]))

        max_value = max(alignment_matrix[i - 1][j - 1] + cost, alignment_matrix[i][j - 1] - gap_penalty,
                        alignment_matrix[i - 1][j] - gap_penalty, 0)

        if max_value == alignment_matrix[i - 1][j - 1] + cost:
            path_matrix[i][j] = 1
            alignment_matrix[i][j] = max_value
        elif max_value == alignment_matrix[i][j - 1] - gap_penalty:
            alignment_matrix[i][j] = max_value
            path_matrix[i][j] = 3
        elif max_value == alignment_matrix[i - 1][j] - gap_penalty:
            alignment_matrix[i][j] = max_value
            path_matrix[i][j] = 2
        else:
            path_matrix[i][j] = 4

    return alignment_matrix, path_matrix


def trace_back():
    i, j = max_index_i_j[0][0], max_index_i_j[1][0]
    edited_seq1 = seq1[:i]
    edited_seq2 = seq2[:j]

    while i > 0 and j > 0:
        if path_matrix[i][j] == 1:
            i -= 1
            j -= 1
        elif path_matrix[i][j] == 2:
            i -= 1
        elif path_matrix[i][j] == 3:
            j -= 1
        else:
            break
    print(edited_seq1[i:])
    print(edited_seq2[j:])


if __name__ == '__main__':
    seq1, seq2 = map(lambda x : str(x.seq),list(SeqIO.parse("rosalind.txt", 'fasta')))

    gap_penalty = 5

    alignment_matrix = find_alignment_matrix()[0]
    path_matrix = find_alignment_matrix()[1]
    print(int(alignment_matrix.max()))

    max_index_i_j = where(alignment_matrix == alignment_matrix.max())

    trace_back()
