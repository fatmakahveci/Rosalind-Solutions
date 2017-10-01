#!/bin/env/python

import itertools

file_name='find_a_median_string.txt'

def hammming_distance(pattern1, pattern2):
	d=0
	for i in xrange(len(pattern1)):
		if pattern1[i]==pattern2[i]:
			d+=1
	return d

def median_string(sequences,k):
    print list(itertools.permutations([A C G T],4))
    # distance = float('inf')
    # median = ""
    # for kmer in :
        # d = hammming_distance(pattern,)
        # if d <= distance:
            # distance = d
            # median = pattern
	# return median

def main():
	file_content=list(open(file_name,'r').read().split('\n'))
	k=int(file_content[0])
	sequences=map(str,file_content[1:])
	median_string(sequences,k)

if __name__ == '__main__':
	main()