#!/bin/env/python

from Bio import SeqIO
from collections import Counter

file_name = 'k_mer_composition.txt'


def partition_k_mers(sequence, k):
    k_mer_list = []
    for idx in range(len(sequence) - k + 1):
        k_mer_list.append(sequence[idx:idx + k])
    return k_mer_list


def main():
    sequence = str(list(SeqIO.parse(file_name, 'fasta'))[0].seq)
    k = 4
    k_mer_list = partition_k_mers(sequence, k)

    counter_list=Counter(k_mer_list)
    value_list=[]
    for item in sorted(counter_list.items()):
        value_list.append(str(item[1]))
    print(' '.join(value_list))

if __name__ == '__main__':
    main()
