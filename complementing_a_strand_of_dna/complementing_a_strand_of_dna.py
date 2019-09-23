#!/usr/bin/env python3.7

if __name__ == "__main__":
    with open("rosalind_dna.txt","r") as file:
		sequence = file.readline()
		complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
		reverse_complement = "".join(complement.get(base) for base in reversed(sequence))
		print(reverse_complement)
		file.close()
