#!/usr/bin/env python3.7

from Bio import SeqIO
from Bio.SubsMat.MatrixInfo import blosum62


def get_max_alignment(seq1, seq2, gap_penalty):
    m = len(seq1)
    n = len(seq2)

    alignment_matrix = {(0, 0): (0, None)}
    alignment_matrix.update({((i, 0), (i * - gap_penalty, (i - 1, 0))) for i in range(1, m + 1)})
    alignment_matrix.update({((0, i), (i * - gap_penalty, (0, i - 1))) for i in range(1, n + 1)})

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = blosum62.get((seq1[i - 1], seq2[j - 1]))

            if cost == None:
                cost = blosum62.get((seq2[j - 1], seq1[i - 1]))

            max_value = max(alignment_matrix[(i - 1, j - 1)][0] + cost, alignment_matrix[(i - 1, j)][0] - gap_penalty, alignment_matrix[(i, j - 1)][0] - gap_penalty)

            if alignment_matrix[(i - 1, j - 1)][0] + cost == max_value:
                alignment_matrix[(i, j)] = (max_value, (i - 1, j - 1))
            elif alignment_matrix[(i - 1, j)][0] - gap_penalty == max_value:
                alignment_matrix[(i, j)] = (max_value, (i - 1, j))
            elif alignment_matrix[(i, j - 1)][0] - gap_penalty == max_value:
                alignment_matrix[(i, j)] = (max_value, (i, j - 1))

    return alignment_matrix[(i, j)][0]


if __name__ == '__main__':
    seq1, seq2 = map(lambda x : str(x.seq), list(SeqIO.parse("rosalind.txt", 'fasta')))

    gap_penalty = 5

    print(get_max_alignment(seq1, seq2, gap_penalty))
