from Bio import SeqIO

from Bio.SubsMat.MatrixInfo import blosum62

if __name__ == '__main__':

    file_name = 'local_alignment_with_affine_gap_penalty.txt'

    sequences = list(SeqIO.parse(file_name, 'fasta'))

    seq1, seq2 = str(sequences[0].seq), str(sequences[1].seq)
    del file_name, sequences

    m, n = len(seq1), len(seq2)

    match_matrix = [[0 for j in range(n + 1)] for i in range(m + 1)]
    x_matrix = [[0 for j in range(n + 1)] for i in range(m + 1)]
    y_matrix = [[0 for j in range(n + 1)] for i in range(m + 1)]

    trace_back_matrix = [[0 for j in range(n + 1)] for i in range(m + 1)]

    gap_opening, gap_extension = -11, -1

    max_score, max_i, max_j = 0, 0, 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = blosum62.get((seq1[i - 1], seq2[j - 1]))
            if cost == None:
                cost = blosum62.get((seq2[j - 1], seq1[i - 1]))

            match_matrix[i][j] = match_matrix[i - 1][j - 1] + cost

            x_matrix[i][j] = max(match_matrix[i - 1][j] + gap_opening,
                                 x_matrix[i - 1][j] + gap_extension)

            y_matrix[i][j] = max(match_matrix[i][j - 1] + gap_opening,
                                 y_matrix[i][j - 1] + gap_extension)

            scores = [0, match_matrix[i][j], x_matrix[i][j], y_matrix[i][j]]
            max_value = max(scores)
            match_matrix[i][j] = max_value
            trace_back_matrix[i][j] = scores.index(max_value)
            if match_matrix[i][j] >= max_score:
                max_i = i
                max_j = j
                max_score = match_matrix[i][j]

    i, j = max_i, max_j
    print(int(max_score))

    del max_score, match_matrix, x_matrix, y_matrix, gap_extension, gap_opening, m, n

    edited_seq1, edited_seq2 = [], []
    while i > 0 and j > 0:
        if int(trace_back_matrix[i][j]) == 3:
            # edited_seq1.append('-')
            edited_seq2.append(seq2[j - 1])
            j -= 1
            continue
        elif int(trace_back_matrix[i][j]) == 2:
            edited_seq1.append(seq1[i - 1])
            # edited_seq2.append('-')
            i -= 1
            continue
        elif int(trace_back_matrix[i][j]) == 1:
            edited_seq1.append(seq1[i - 1])
            edited_seq2.append(seq2[j - 1])
            i -= 1
            j -= 1
            continue
        else:
            break

    print(''.join(reversed(edited_seq1)) + '\n' + ''.join(reversed(edited_seq2)))
