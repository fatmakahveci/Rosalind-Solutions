#!/bin/env/python

num_a=0;num_c=0;num_g=0;num_t=0

file_content=open('counting_dna_nucleotides.txt','r').read()

for i in xrange(len(file_content)):
	if file_content[i]=='A':
		num_a+=1
	elif file_content[i]=='C':
		num_c+=1
	elif file_content[i]=='G':
		num_g+=1
	elif file_content[i]=='T':
		num_t+=1
print str(num_a)+' '+str(num_c)+' '+str(num_g)+' '+str(num_t)