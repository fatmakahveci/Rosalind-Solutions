#!/bin/env/python

if __name__ == "__main__":
    file = open("rosalind_dna.txt","r")
    dna_string = str(file.readlines()).strip()
    base_count_list = map(str, [dna_string.count('A'),dna_string.count('C'),dna_string.count('G'),dna_string.count('T')])
    print(' '.join(base_count_list))
    file.close()
