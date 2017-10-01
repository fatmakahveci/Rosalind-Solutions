#!/bin/env python

from Bio import SeqIO
from io import StringIO

file_name='/home/usario/Documents/rosalind/finding_a_shared_motif/finding_a_shared_motif.txt'

def find_motif(sequences):
	shortest_sequence_index = sequences.index(min(sequences, key=len))
	shortest_sequence = sequences[shortest_sequence_index]
	other_sequences = sequences[:shortest_sequence_index] + sequences[shortest_sequence_index + 1:]

	motif = ''
	for i in range(len(shortest_sequence)):
		for j in range(len(shortest_sequence), i + len(motif), -1):

			first_sequence = shortest_sequence[i:j]
			is_all_matched = True
			for second_sequence in other_sequences:
				if first_sequence not in second_sequence:
					is_all_matched = False
					break

			if is_all_matched:
				motif = first_sequence
				break
	return(motif)

def main():
	sequence_list=list(SeqIO.parse(StringIO(open(file_name,'r').read()),'fasta'))
	sequences=[]
	for i in range(len(sequence_list)):
		sequences.append(str(sequence_list[i].seq))

	print(find_motif(sequences))

if __name__ == '__main__':
	main()
