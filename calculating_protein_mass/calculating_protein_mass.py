#!/bin/env/python

file_name = 'calculating_protein_mass.txt'


def read_table(file_name):
    amino_acid = []
    amino_acid_mass = []

    for line in open(file_name, 'r').read().split('\n'):
        line = line.replace(' ', '')
        amino_acid.append(line[0])
        amino_acid_mass.append(float(line[1:]))
    return amino_acid, amino_acid_mass


def read_protein(file_name):
    protein = open(file_name, 'r').read()
    return protein


def main():
    amino_acid, amino_acid_mass = read_table('../tables/monoisotopic_mass_table.txt')
    protein = read_protein(file_name)

    sum = 0

    for i in range(len(protein)):
        sum += amino_acid_mass[amino_acid.index(protein[i])]

    print(round(sum, 3))


if __name__ == '__main__':
    main()
