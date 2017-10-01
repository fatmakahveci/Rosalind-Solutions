#!/bin/env/python

import sys

file_content=open('transcribing_dna_into_rna.txt','r').read()

for i in xrange(len(file_content)):
	if file_content[i]=='T':
		sys.stdout.write("U")
	else:
		sys.stdout.write(file_content[i])
print ""