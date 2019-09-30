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

	protein = open("rosalind.txt", 'r').read()
	codon_value_set = list(set(rna_codon_dict.values()))
	count = [0] * len(codon_value_set)
	i = 0
	for value in codon_value_set:
	    for element in rna_codon_dict.values():
	        if element == value:
	            count[i] += 1
	    i += 1
    
	stop_codon = count[codon_value_set.index('Stop')]
	result = stop_codon
	for p in protein:
	    result *= count[codon_value_set.index(p)]
	print(result % 1000000)
