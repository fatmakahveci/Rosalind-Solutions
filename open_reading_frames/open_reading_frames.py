#!/bin/env/python3.7

from Bio.Seq import Seq
from Bio import SeqIO


def translate_codon(codon):
    if len(codon) == 3:
        return str(Seq(codon).translate())
    else:
        return None

def orf(sequence):
    orfs = []
    start_positions = [i for i in range(len(sequence)) if translate_codon(sequence[i:i + 3]) == 'M' and translate_codon(sequence[i:i + 3]) != None]

    for i in start_positions:
        is_found_stop = False
        protein_sequence = ''

        for j in range(i, len(sequence), 3):
            if translate_codon(sequence[j:j + 3]) == None:
                break
            if translate_codon(sequence[j:j + 3]) == '*':
                is_found_stop = True
                break
            protein_sequence += translate_codon(sequence[j:j + 3])
        if is_found_stop:
            orfs.append(protein_sequence)

    return orfs


if __name__ == "__main__":
    rna_sequence = str(list(SeqIO.parse("rosalind.txt", 'fasta'))[0].seq)

    rna_orf = orf(rna_sequence)
    reverse_rna_orf = orf(str(Seq(rna_sequence).reverse_complement()))

    orf_set = set(rna_orf + reverse_rna_orf)

    print('\n'.join(orf_set))
