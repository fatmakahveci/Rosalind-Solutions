#!/bin/env/python

file_name = 'inferring_mrna_from_protein.txt'


def codon_alphabet():
    alphabet_file_content = open('../tables/rna_codon_table.txt', 'r').read().replace('\n', '').replace('\t','').replace(' ','')
    dict_codon = {}
    i = 0
    while i <= len(alphabet_file_content) - 4:
        s = alphabet_file_content[i:i + 3]
        r = alphabet_file_content[i + 3]
        if r == 'X':
            dict_codon[s] = 'Stop'
        else:
            dict_codon[s] = r
        i += 4
    return dict_codon


def main():
    protein = open(file_name, 'r').read()
    codon_value_set = list(set(codon_alphabet().values()))
    count = [0] * len(codon_value_set)
    i = 0
    for value in codon_value_set:
        for element in codon_alphabet().values():
            if element == value:
                count[i] += 1
        i += 1
    
    stop_codon = count[codon_value_set.index('Stop')]
    result = stop_codon
    for p in protein:
        result *= count[codon_value_set.index(p)]
    print(result % 1000000)


if __name__ == '__main__':
    main()

