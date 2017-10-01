#!/bin/env/python

from StringIO import StringIO
from Bio import SeqIO

file_name='computing_gc_content.txt'

def computing_gc_content():
	
	sequences=list(SeqIO.parse(StringIO(open(file_name,'r').read()), "fasta"))

	max_gc_content=0
	max_gc_content_id=''
	for i in xrange(len(sequences)):
		seq=sequences[i].seq
		num_a=0;num_c=0;num_g=0;num_t=0
		for j in xrange(len(seq)):
			nucl=seq[j]
			if nucl == 'A':
				num_a+=1
			elif nucl == 'C':
				num_c+=1
			elif nucl == 'G':
				num_g+=1
			elif nucl == 'T':
				num_t+=1
		gc_content=float(num_c+num_g)/float(num_a+num_c+num_g+num_t)
		
		if gc_content >= max_gc_content:
			max_gc_content=gc_content
			max_gc_content_id=sequences[i].id
	
	print max_gc_content_id
	print("%.6f" % (max_gc_content*100))

def main():
	computing_gc_content()

if __name__ == '__main__':
	main()