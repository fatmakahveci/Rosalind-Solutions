#!/bin/env/python

from Bio import SeqIO

file_name = 'edit_distance.txt'


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


def main():
    sequences = list(SeqIO.parse(file_name, 'fasta'))

    seq1 = sequences[1].seq
    seq2 = sequences[0].seq

    print(calculate_edit_distance(seq1, seq2))


if __name__ == '__main__':
    main()
