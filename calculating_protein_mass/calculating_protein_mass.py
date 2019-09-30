#!/bin/env/python3.7


if __name__ == '__main__':
    
    amino_acid = []
    amino_acid_mass = []

    for line in open('monoisotopic_mass_table.txt', 'r').read().split('\n'):
        line = line.replace(' ', '')
        amino_acid.append(line[0])
        amino_acid_mass.append(float(line[1:]))

    protein = open("rosalind.txt","r").read()

    sum = 0

    for i in range(len(protein)):
        sum += amino_acid_mass[amino_acid.index(protein[i])]

    print(round(sum, 3))
