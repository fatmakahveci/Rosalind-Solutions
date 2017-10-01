#!/bin/env/python

import sys
from Bio import SeqIO
from StringIO import StringIO

file_name='consensus_and_profile.txt'

def main():

	sequences=list(SeqIO.parse(StringIO(open(file_name,'r').read()),'fasta'))

	size=len(sequences[0].seq)	
	a_array=[0]*size
	c_array=[0]*size
	g_array=[0]*size
	t_array=[0]*size

	for i in xrange(len(sequences)):
		seq=sequences[i].seq
		for j in xrange(size):
			if seq[j] == 'A':
				a_array[j] += 1
			elif seq[j] == 'C':
				c_array[j] += 1
			elif seq[j] == 'G':
				g_array[j] += 1
			elif seq[j] == 'T':
				t_array[j] += 1

	for i in xrange(size):
		max_value=max(a_array[i],c_array[i],g_array[i],t_array[i])
		if max_value==a_array[i]:
			sys.stdout.write('A')
		elif max_value==c_array[i]:
			sys.stdout.write('C')
		elif max_value==g_array[i]:
			sys.stdout.write('G')
		elif max_value==t_array[i]:
			sys.stdout.write('T')
	print ''
	print('A: '+' '.join(map(str,a_array)))
	print('C: '+' '.join(map(str,c_array)))
	print('G: '+' '.join(map(str,g_array)))
	print('T: '+' '.join(map(str,t_array)))

if __name__ == '__main__':
	main()