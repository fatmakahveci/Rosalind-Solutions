#!/bin/env/python

import math,itertools,sys

def main():
	variables=int(open('enumerating_gene_orders.txt','r').read().strip())
	print math.factorial(variables)
	for line in list(itertools.permutations(range(1,variables+1),variables)):
		for i in xrange(variables):
			sys.stdout.write(str(line[i]))
			if i != variables:
				sys.stdout.write(' ')
		print ''

if __name__ == '__main__':
	main()