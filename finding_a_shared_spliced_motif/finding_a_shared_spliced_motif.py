#!/usr/bin/env python3.7

from Bio import SeqIO

import numpy


if __name__ == '__main__':
    sequences = list(SeqIO.parse("rosalind.txt", 'fasta'))

    seq1 = sequences[0].seq
    seq2 = sequences[1].seq

    m = len(seq1)
    n = len(seq2)

    lcs_matrix = numpy.zeros((m + 1, n + 1))
    path_matrix = numpy.zeros((m + 1, n + 1))

    for row in range(m):
        for column in range(n):
            if seq1[row] == seq2[column]:
                path_matrix[row + 1][column + 1] = 1
                lcs_matrix[row + 1][column + 1] = lcs_matrix[row][column] + 1
            else:
                lcs_matrix[row + 1][column + 1] = max(lcs_matrix[row][column + 1], lcs_matrix[row + 1][column])
                if lcs_matrix[row + 1][column + 1] == lcs_matrix[row][column + 1]:
                    path_matrix[row + 1][column + 1] = 2
                else:
                    path_matrix[row + 1][column + 1] = 3

    row = m
    column = n
    lcs = []
    while row > 0 and column > 0:
        if path_matrix[row][column] == 1:
            lcs.append(seq1[row - 1])
            row -= 1
            column -= 1
        elif path_matrix[row][column] == 2:
            row -= 1
        else:
            column -= 1

    ordered_lcs = []
    for i in range(len(lcs) - 1, -1, -1):
        ordered_lcs.append(lcs[i])
    print(''.join(ordered_lcs))
