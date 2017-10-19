#!/usr/bin/env python

from Bio import SeqIO
from numpy import zeros

file_name = 'edit_distance_alignment.txt'


def indel(sequence, i):
    return sequence[:i] + '-' + sequence[i:]


def edit_alignment(seq1, seq2):
    m = len(seq1)
    n = len(seq2)

    edit_distance_matrix = zeros((m + 1, n + 1), dtype=int)
    trace_back_matrix = zeros((m + 1, n + 1), dtype=int)

    for i in range(0, m + 1):
        for j in range(0, n + 1):
            if j == 0:
                edit_distance_matrix[i][0] = i
            elif i == 0:
                edit_distance_matrix[0][j] = j
            else:
                if (not (seq1[i - 1] is seq2[j - 1])):
                    edit_distance_matrix[i - 1][j - 1] += 1
                scores = [edit_distance_matrix[i - 1][j - 1], edit_distance_matrix[i - 1][j] + 1,
                          edit_distance_matrix[i][j - 1] + 1]
                edit_distance_matrix[i][j] = min(scores)
                trace_back_matrix[i][j] = scores.index(edit_distance_matrix[i][j])

    edited_seq1 = seq1
    edited_seq2 = seq2
    i = m
    j = n

    while i > 0 and j > 0:
        if trace_back_matrix[i][j] == 1:
            i -= 1
            edited_seq2 = indel(edited_seq2, j)
        elif trace_back_matrix[i][j] == 2:
            j -= 1
            edited_seq1 = indel(edited_seq1, i)
        else:
            i -= 1
            j -= 1

    print(str(edit_distance_matrix[m][n]))
    return edited_seq1, edited_seq2


def main():
    sequences = list(SeqIO.parse(file_name, 'fasta'))

    seq1 = sequences[0].seq
    seq2 = sequences[1].seq

    edited_sequences = edit_alignment(seq1, seq2)
    print(edited_sequences[0])
    print(edited_sequences[1])


if __name__ == '__main__':
    main()
