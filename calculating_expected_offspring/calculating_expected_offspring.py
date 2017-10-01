#!/bin/env python

def get_sequences(file_name):
	return open(file_name,'r').read().split(' ')

def calculating_expected_offspring(file_name):
	genotype_list = map(float,get_sequences(file_name))
	total=sum(genotype_list)
	return 2*(genotype_list[0]+genotype_list[1]+genotype_list[2]+genotype_list[3]*3/4+genotype_list[4]/2)

def main():
	print str(calculating_expected_offspring('calculating_expected_offspring.txt'))

if __name__ == '__main__':
	main()