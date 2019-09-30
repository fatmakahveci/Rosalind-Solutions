#!/bin/env python3.7

if __name__ == '__main__':
	genotype_list = map(float, open("rosalind.txt", 'r').read().split(' '))

	print(str(2 * (genotype_list[0] + genotype_list[1] + genotype_list[2] + genotype_list[3] * 3 / 4 + genotype_list[4] / 2)))
