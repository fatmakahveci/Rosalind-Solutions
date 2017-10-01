#!/bin/env/python

import sys

rna_file_name='translating_rna_into_protein.txt'
alphabet_file_name='rna_codon_table.txt'

rna=[]
seq=[]

def readfile(file_name):
	return open(file_name,'r').read()

def create_protein_alphabet():
	alphabet_file_content=readfile(alphabet_file_name).replace('\n','').replace('\t','').replace(' ','')
	i=0
	while i <= len(alphabet_file_content)-4:
		s=alphabet_file_content[i:i+3]
		r=alphabet_file_content[i+3]
		seq.append(s)
		if r == 'X':
			rna.append('Stop')
		else:
			rna.append(r)
		i+=4

def convert_rna_into_protein():
	rna_seq=readfile(rna_file_name)
	i=0
	while i < len(rna_seq)-3:
		sys.stdout.write(rna[seq.index(rna_seq[i:i+3])])
		i+=3
	print ''

def main():
	create_protein_alphabet()
	convert_rna_into_protein()

if __name__ == '__main__':
	main()