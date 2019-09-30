#!/bin/env/python3.7


if __name__ == '__main__':

	with open("rna_codon_table.txt", 'r') as file:
		item_list = file.read().split()
		file.close()
	
	rna_codon_dict = {}
	i = 0
	while i < len(item_list) - 1:
		rna_codon_dict[item_list[i]] = item_list[i+1]
		i += 1

	with open("rosalind.txt", "r") as file:
		rna = str(file.readline().strip())
    	file.close()

	protein_list = []
	i = 0
	while i < len(rna):
		protein = rna_codon_dict[rna[i:i+3]]
		protein_list.append(protein)
		i += 3
	print(''.join(protein_list))
