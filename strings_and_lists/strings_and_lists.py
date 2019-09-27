#!/usr/bin/env python3.7

if __name__ == "__main__":

	with open("rosalind.txt", "r") as file:
		string = file.readline()
		a, b, c, d = map(int, file.readline().split(' '))

		print(string[a:b+1]+' '+string[c:d+1])

		file.close()
