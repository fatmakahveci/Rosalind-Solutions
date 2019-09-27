#!/usr/bin/env python3.7

from sys import maxsize
from itertools import product


def find_all_possible_kmers():
	return [''.join(c) for c in product(['A', 'C', 'G', 'T'], repeat=k)]

def hamming_dist(seq1, seq2):
	return len(list(filter(lambda base: base[0] != base[1], zip(seq1, seq2))))

def total_dist(pattern, seq_list):
	dist = 0
	for seq in seq_list:
		min_hamming_dist = maxsize
		last_k_mer_idx = len(seq) - k + 1

		for i in range(last_k_mer_idx):
			min_hamming_dist = min(min_hamming_dist, hamming_dist(pattern, seq[i:i + k]))
		dist += min_hamming_dist
	return dist

def find_median_string(seq_list):
	median_string = 'A' * k
	median_string_dist = k
	for k_mer in find_all_possible_kmers():
		d = total_dist(k_mer, seq_list)
		if d <= median_string_dist:
			median_string_dist = d
			median_string = k_mer

	return median_string

if __name__ == "__main__":

	with open("rosalind.txt", "r") as file:
		k = int(file.readline())

		print(find_median_string(file.readlines()))

		file.close()
