#!/usr/bin/env python3.7

from Bio import SeqIO


def calculate_edit_distance(seq1, seq2):
    m = len(seq1)
    n = len(seq2)

    edit_distance_matrix = [[0] * (n + 1) for i in range(m + 1)]

    for row in range(m + 1):
        for column in range(n + 1):
            if row == 0:
                edit_distance_matrix[row][column] = column
            elif column == 0:
                edit_distance_matrix[row][column] = row
            elif seq1[row - 1] == seq2[column - 1]:
                edit_distance_matrix[row][column] = edit_distance_matrix[row - 1][column - 1]
            else:
                edit_distance_matrix[row][column] = 1 + min(edit_distance_matrix[row][column - 1],
                                                            edit_distance_matrix[row - 1][column],
                                                            edit_distance_matrix[row - 1][column - 1])
    return edit_distance_matrix[m][n]


if __name__ == '__main__':
    seq1, seq2 = map(lambda x: str(x.seq), list(SeqIO.parse("rosalind.txt", 'fasta')))

    print(calculate_edit_distance(seq1, seq2))
