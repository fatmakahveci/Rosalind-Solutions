#!/bin/env/python

import sys

from Bio import SeqIO
from StringIO import StringIO

file_name='open_reading_frames.txt'

def main():
	rna_sequence=list(SeqIO.parse(StringIO(open(file_name,'r').read()),'fasta'))[0].seq.transcribe()
	reverse_complement_rna_sequence=list(SeqIO.parse(StringIO(open(file_name,'r').read()),'fasta'))[0].seq.transcribe().reverse_complement()
	print reverse_complement_rna_sequence
	i=0
	while i <= len(rna_sequence)-3:
		codon=rna_sequence[i:i+3].translate()
		
		if codon == 'M':
			sys.stdout.write(str(rna_sequence[i:].translate()))
			print ''		
		i+=3

if __name__ == '__main__':
	main()