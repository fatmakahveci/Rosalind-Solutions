#!/usr/bin/env python3.7

if __name__ == "__main__":

	with open("rosalind.txt", "r") as file:

		file.readline()
		sequence = str(''.join(file.readlines())).replace('\n','')
		print(sequence)
		complements = {'A':'T', 'T':'A', 'G':'C', 'C':'G'}
		n = len(sequence)

		for start in range(n):
			for k in range(4,13): # k := k-mer length
				if start + k > n:
					continue
				first_sequence = sequence[start:start+k]
				# reverse complement
				second_sequence = ''.join([complements[base] for base in first_sequence[::-1]])

				if first_sequence == second_sequence:
					print(' '.join(map(str, [start + 1, k])))

		file.close()
