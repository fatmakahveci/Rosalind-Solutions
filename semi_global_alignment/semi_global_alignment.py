#!/bin/env/python

from Bio import SeqIO
from itertools import product
from numpy import zeros, where

file_name = 'semi_global_alignment.txt'


def find_alignment_matrix(seq1, seq2, m, n, gap_penalty):
    alignment_matrix = zeros((m + 1, n + 1))
    path_matrix = zeros((m + 1, n + 1))

    for i in range(0, m + 1):
        alignment_matrix[i][0] = i * (-gap_penalty)
        path_matrix[i][0] = 4

    for j in range(0, n + 1):
        alignment_matrix[0][j] = j * (-gap_penalty)
        path_matrix[0][j] = 4

    for i, j in product(range(1, m + 1), range(1, n + 1)):
        if seq1[i - 1] == seq2[j - 1]:
            cost = 1
        else:
            cost = -1
        max_value = max(alignment_matrix[i - 1][j - 1] + cost, alignment_matrix[i][j - 1] - gap_penalty)

        if max_value == alignment_matrix[i - 1][j - 1] + cost:
            path_matrix[i][j] = 1
            alignment_matrix[i][j] = max_value
        elif max_value == alignment_matrix[i][j - 1] - gap_penalty:
            alignment_matrix[i][j] = max_value
            path_matrix[i][j] = 3

    return alignment_matrix, path_matrix


def trace_back(trace_back_matrix, i, j, seq1, seq2):
    edited_seq1, edited_seq2 = [], []
    while i > 0 and j > 0:
        if int(trace_back_matrix[i][j]) == 3:
            edited_seq1.append('-')
            edited_seq2.append(seq2[j - 1])
            j -= 1
            continue
        elif int(trace_back_matrix[i][j]) == 1:
            edited_seq1.append(seq1[i - 1])
            edited_seq2.append(seq2[j - 1])
            i -= 1
            j -= 1
            continue

    print(''.join(reversed(edited_seq1)) + '\n' + ''.join(reversed(edited_seq2)))


def main():
    sequences = list(SeqIO.parse(file_name, 'fasta'))

    seq1, seq2 = str(sequences[0].seq), str(sequences[1].seq)
    n, m = len(seq1), len(seq2)
    gap_penalty = 1

    alignment_matrix = find_alignment_matrix(seq1, seq2, n, m, gap_penalty)[0]
    path_matrix = find_alignment_matrix(seq1, seq2, n, m, gap_penalty)[1]
    print(int(alignment_matrix.max()))

    trace_back(path_matrix, n, m, seq1, seq2)


if __name__ == '__main__':
    main()
