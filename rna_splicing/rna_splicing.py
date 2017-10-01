#!/bin/env/python

from Bio.Seq import Seq
from Bio.Alphabet import generic_dna
from Bio import SeqIO
from StringIO import StringIO

def main():
	sequences=list(SeqIO.parse(StringIO(open('rna_splicing.txt','r').read().strip()),'fasta'))
	
	dna_sequence=str(sequences[0].seq)
	introns=[]
	for i in xrange(1,len(sequences)):
		introns.append(str(sequences[i].seq))
	for intron in introns:
		dna_sequence=dna_sequence.replace(intron,'')
	coding_dna = Seq(dna_sequence, generic_dna)
	translated_dna=coding_dna.translate(to_stop=True)
	print str(translated_dna)
	
if __name__ == '__main__':
	main()