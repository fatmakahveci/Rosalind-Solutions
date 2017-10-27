#!/bin/env/python

from Bio import SeqIO

file_name = 'locating_restriction_sites.txt'


def find_reverse_complement(sequence):
    dict = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    for i in range(len(sequence)):
        sequence = sequence[:i] + dict.get(sequence[i]) + sequence[i + 1:]
    return sequence[::-1]


def divide_into_kmers(sequence, k):
    k_mer_list = []
    for i in range(len(sequence) - k + 1):
        k_mer_list.append(sequence[i:i + k])
    return k_mer_list


def main():
    sequence = str(list(SeqIO.parse(file_name, 'fasta'))[0].seq)
    for k in range(4, 13):
        k_mer_list = divide_into_kmers(sequence, k)
        for index, k_mer in enumerate(k_mer_list):
            reverse_k_mer = find_reverse_complement(k_mer)
            if k_mer == reverse_k_mer:
                print(index+1, k)


if __name__ == '__main__':
    main()
