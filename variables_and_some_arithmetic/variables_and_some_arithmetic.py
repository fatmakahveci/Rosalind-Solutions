#!/usr/bin/env python3.7

from math import sqrt


if __name__ == "__main__":

	with open("rosalind.txt", "r") as file:
		m, n = map(int, file.readline().split(' '))
		print(str(m**2+n**2))

		file.close()
