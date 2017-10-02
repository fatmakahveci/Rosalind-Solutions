#!/bin/env/python

import itertools
import sys

file_name = 'find_a_median_string.txt'


def find_all_possible_kmers(k):
    nucleotides = ['A', 'C', 'G', 'T']
    nucleotide_combinations = list(itertools.product(nucleotides, repeat=k))
    for i in range(len(nucleotide_combinations)):
        nucleotide_combinations[i] = ''.join(nucleotide_combinations[i])
    return nucleotide_combinations


def hamming_distance(pattern1, pattern2):
    d = 0
    for i in range(len(pattern1)):
        if pattern1[i] != pattern2[i]:
            d += 1
    return d


def total_distance(pattern, sequences,k):
    distance = 0
    for sequence in sequences:
        min_hamming = sys.maxsize
        for i in range(len(sequence) - k + 1):
            min_hamming = min(min_hamming, hamming_distance(pattern, sequence[i:i + k]))
        distance += min_hamming
    return distance


def median_string(sequences, k):
    best_pattern = sequences[0][:k]
    best_distance = k
    for kmer in find_all_possible_kmers(k):
        d = total_distance(kmer, sequences,k)
        if d <= best_distance:
            best_distance = d
            best_pattern = kmer
    return best_pattern

def main():
    file_content = list(open(file_name, 'r').read().split('\n'))
    k = int(file_content[0])
    sequences = file_content[1:]
    print(median_string(sequences, k))


if __name__ == '__main__':
    main()
