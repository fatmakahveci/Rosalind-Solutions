#!/bin/env/python

from Bio import SeqIO
from Bio.SubsMat.MatrixInfo import blosum62
from numpy import zeros
from itertools import product
from sys import maxsize

file_name = 'global_alignment_with_scoring_matrix_and_affine_gap_penalty.txt'

gap_opening_penalty = -11
gap_extension_penalty = -1


def blosum_score(seq1, seq2, i, j):
    cost = blosum62.get((seq1[i], seq2[j]))

    if cost == None:
        cost = blosum62.get((seq2[j], seq1[i]))
    return cost


def indel(seq, i):
    return seq[:i] + '-' + seq[i:]


def global_align_with_affine(seq1, seq2, m, n):
    match_matrix = zeros((m + 1, n + 1))
    gap_seq1_matrix = zeros((m + 1, n + 1))
    gap_seq2_matrix = zeros((m + 1, n + 1))

    trace_back_match_matrix = zeros((m + 1, n + 1))
    trace_back_gap_seq1_matrix = zeros((m + 1, n + 1))
    trace_back_gap_seq2_matrix = zeros((m + 1, n + 1))

    for i in range(1, m + 1):
        match_matrix[i][0] = gap_opening_penalty + gap_extension_penalty * (i - 1)
        gap_seq1_matrix[i][0] = -maxsize
        gap_seq2_matrix[i][0] = -maxsize

    for j in range(1, n + 1):
        match_matrix[0][j] = gap_opening_penalty + gap_extension_penalty * (j - 1)
        gap_seq1_matrix[0][j] = -maxsize
        gap_seq2_matrix[0][j] = -maxsize

    for i, j in product(range(m + 1), range(n + 1)):
        gap_seq1_cost = [match_matrix[i - 1][j] + gap_opening_penalty,
                         gap_seq1_matrix[i - 1][j] + gap_extension_penalty]
        gap_seq1_matrix[i][j] = max(gap_seq1_cost)
        trace_back_gap_seq1_matrix[i][j] = gap_seq1_cost.index(gap_seq1_matrix[i][j])

        gap_seq2_cost = [match_matrix[i][j - 1] + gap_opening_penalty,
                         gap_seq2_matrix[i][j - 1] + gap_extension_penalty]
        gap_seq2_matrix[i][j] = max(gap_seq2_cost)
        trace_back_gap_seq2_matrix[i][j] = gap_seq2_cost.index(gap_seq2_matrix[i][j])

        match_cost = [match_matrix[i - 1][j - 1] + blosum_score(seq1, seq2, i - 1, j - 1),
                      gap_seq1_matrix[i][j],
                      gap_seq2_matrix[i][j]]
        match_matrix[i][j] = max(match_cost)
        trace_back_match_matrix[i][j] = match_cost.index(match_matrix[i][j])

    seq1_align, seq2_align = seq1, seq2

    scores = [gap_seq1_matrix[i][j], gap_seq2_matrix[i][j], match_matrix[i][j]]
    max_score = max(scores)
    trace_back = scores.index(max_score)
    
    i, j = m, n

    while i > 0 and j > 0:
        if trace_back == 0:
            if trace_back_gap_seq1_matrix[i][j] == 0:
                trace_back = 2
            i -= 1
            seq2_align = indel(seq2_align, j)

        elif trace_back == 1:
            if trace_back_gap_seq2_matrix[i][j] == 0:
                trace_back = 2
            j -= 1
            seq1_align = indel(seq1_align, i)

        elif trace_back == 2:
            if trace_back_match_matrix[i][j] == 1:
                trace_back = 0
            elif trace_back_match_matrix[i][j] == 2:
                trace_back = 1
            else:
                i -= 1
                j -= 1

    for remaining in range(i):
        seq2_align = indel(seq2_align, 0)
    for remaining in range(j):
        seq1_align = indel(seq1_align, 0)

    return int(max_score), seq1_align, seq2_align


def main():
    sequences = list(SeqIO.parse(file_name, 'fasta'))

    seq1, seq2 = sequences[0].seq, sequences[1].seq

    alignment = global_align_with_affine(seq1, seq2, len(seq1), len(seq2))

    print(str(alignment[0]) + '\n' + alignment[1] + '\n' + alignment[2])


if __name__ == '__main__':
    main()
