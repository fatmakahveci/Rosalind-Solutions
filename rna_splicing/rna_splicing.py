#!/usr/bin/env python3.7

from Bio.Seq import Seq
from Bio.Alphabet import generic_dna
from Bio import SeqIO


if __name__ == '__main__':
    sequences = list(SeqIO.parse("rosalind.txt", 'fasta'))

    dna_sequence = str(sequences[0].seq)
    introns = []
    for i in range(1, len(sequences)):
        introns.append(str(sequences[i].seq))
    for intron in introns:
        dna_sequence = dna_sequence.replace(intron, '')
    coding_dna = Seq(dna_sequence, generic_dna)
    translated_dna = coding_dna.translate(to_stop=True)
    print(str(translated_dna))
