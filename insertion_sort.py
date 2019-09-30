#!/bin/env/python

def swap(arr, pos1, pos2):
	arr[pos1], arr[pos2] = arr[pos2], arr[pos1]
	return arr
	

def insertion_sort_swap(arr):
	n_swap = 0
	for i in range(1, n):
		k = i
		while k > 0 and arr[k] < arr[k-1]:
			swap(arr, k-1, k)
			n_swap += 1
			k -= 1
	return n_swap

if __name__ == "__main__":

	with open("rosalind.txt", 'r') as file:
		n = int(file.readline())
		arr = map(int, file.readline().split(' '))

		print(str(insertion_sort_swap(arr)))

		file.close()
