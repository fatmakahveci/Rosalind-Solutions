#!/bin/env/python

from Bio.Seq import Seq
from Bio.Alphabet import generic_dna
from Bio import SeqIO
from io import StringIO

file_name='rna_splicing.txt'

def main():
    sequences = list(SeqIO.parse(StringIO(open(file_name, 'r').read().strip()), 'fasta'))

    dna_sequence = str(sequences[0].seq)
    introns = []
    for i in range(1, len(sequences)):
        introns.append(str(sequences[i].seq))
    for intron in introns:
        dna_sequence = dna_sequence.replace(intron, '')
    coding_dna = Seq(dna_sequence, generic_dna)
    translated_dna = coding_dna.translate(to_stop=True)
    print(str(translated_dna))


if __name__ == '__main__':
    main()