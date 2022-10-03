#!/usr/bin/env python3.7

import numpy as np


def needleman_wunsch(seq1, seq2, match_score, mismatch_penalty, gap_penalty):
	m = len(seq1)
	n = len(seq2)

	V = np.zeros((m+1,n+1))
	P = np.zeros((m+1,n+1))

	for i in range(m+1):
		for j in range(n+1):
			
			if i >= 0 and j == 0:
				V[i][j] = gap_penalty * i
				P[i][j] = 1

			elif i == 0 and j >= 0:
				V[i][j] = gap_penalty * j
				P[i][j] = 2

			else:
				if seq1[i-1] == seq2[j-1]:
					match_case = V[i-1][j-1] + match_score
				else:
					match_case = V[i-1][j-1] + mismatch_penalty

				gap_in_first_case = V[i][j-1] + gap_penalty

				gap_in_second_case = V[i-1][j] + gap_penalty

				value_list = [match_case, gap_in_first_case, gap_in_second_case]
			
				max_value = value_list.index(max(value_list))

				V[i][j] = value_list[max_value]
				P[i][j] = max_value

	i = m
	j = n

	aligned_seq1 = ""
	aligned_seq2 = ""
	score = 0	
	while i > 0 and j > 0:

		if P[i][j] == 0:
			aligned_seq1 += seq1[i-1]
			aligned_seq2 += seq2[j-1]
			i -= 1
			j -= 1
			score += match_score

		elif P[i][j] == 2:
			aligned_seq1 += seq1[i-1]
			aligned_seq2 += "-"
			i -= 1
			score += gap_penalty

		elif P[i][j] == 1:
			aligned_seq1 += "-"
			aligned_seq2 += seq2[j-1]
			j -= 1
			score += gap_penalty

	if i > 0:
		aligned_seq1 += seq1[i:]
		aligned_seq2 += "-"
		i -= 1
		score += gap_penalty

	if j > 0:
		aligned_seq1 += "-"
		aligned_seq2 += seq2[j:]
		j -= 1
		score += gap_penalty
	
	seq1 = ''.join(reversed(aligned_seq1))
	seq2 = ''.join(reversed(aligned_seq2))
	
	return [score, seq1, seq2]


if __name__ == "__main__":
	seq1 = "ACGT"
	seq2 = "ACTAAAAA"

	match_score = 1
	mismatch_penalty = -5
	gap_penalty = -1
	
	score, aln_seq1, aln_seq2 = needleman_wunsch(seq1, seq2, match_score, mismatch_penalty, gap_penalty)
