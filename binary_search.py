#!/bin/env/python

def binary_search(arr, item, min_idx, max_idx):
	if max_idx < min_idx:
		return -1

	mid_idx = int((min_idx + max_idx) / 2)
	if arr[mid_idx] > item:
		return binary_search(arr, item, min_idx, mid_idx-1)
	elif arr[mid_idx] == item:
		return mid_idx
	
	return binary_search(arr, item, mid_idx+1, max_idx)

if __name__ == "__main__":

	with open("rosalind.txt", 'r') as file:
		file.readline();file.readline()

		arr = map(int, file.readline().split(' '))
		search_arr = map(int, file.readline().split(' '))
		
		idx_arr = []
		for item in search_arr:
			idx = binary_search(arr, item, 0, len(arr))
			if idx != -1:
				idx_arr.append(idx+1)
			else:
				idx_arr.append(-1)

		print(' '.join(map(str, idx_arr)))

		file.close()
