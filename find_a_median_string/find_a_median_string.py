#!/bin/env/python

import itertools

file_name = 'find_a_median_string.txt'

def hamming_distance(pattern1, pattern2):
    d = 0
    for i in range(len(pattern1)):
        if pattern1[i] == pattern2[i]:
            d += 1
    return d


def find_all_possible_kmers(sequences, k):
    nucleotides = ['A', 'C', 'G', 'T']
    nucleotide_combinations = list(itertools.product(nucleotides, repeat=k))
    for i in range(len(nucleotide_combinations)):
        nucleotide_combinations[i] = ''.join(nucleotide_combinations[i])
    return nucleotide_combinations


def median_string(sequences, k):
    all_kmers = find_all_possible_kmers(sequences, k)
    count = [0] * len(all_kmers)
    for i in range(len(sequences)):
        sequence = sequences[i]
        for j in range(len(sequence) - k):
            seq = sequence[j:j + k]
            count[all_kmers.index(seq)] += 1
        print
    print(all_kmers[count.index(max(count))])


def main():
    file_content = list(open(file_name, 'r').read().split('\n'))
    k = int(file_content[0])
    sequences = file_content[1:]
    median_string(sequences, k)


if __name__ == '__main__':
    main()
