#!/bin/env/python

# transitions := purine -> purine a <-> g or pyrimidine -> pyrimidine c <-> t
# transversions := purine -> pyrimidine  or pyrimidine -> purine

from Bio import SeqIO
from io import StringIO

file_name = 'transitions_and_transversions.txt'


def main():
    sequence_list = list(SeqIO.parse(StringIO(open(file_name, 'r').read()), 'fasta'))
    first_sequence = sequence_list[0].seq
    second_sequence = sequence_list[1].seq

    purine = set(['A', 'G'])
    pyrimidine = set(['C', 'T'])

    count_transitions = 0
    count_transversions = 0

    for i in range(len(first_sequence)):
        if first_sequence[i] != second_sequence[i]:
            if (first_sequence[i] in purine and second_sequence[i] in purine) or (
                            first_sequence[i] in pyrimidine and second_sequence[i] in pyrimidine):
                count_transitions += 1
            else:
                count_transversions += 1
    print(float(count_transitions) / float(count_transversions))


if __name__ == '__main__':
    main()
