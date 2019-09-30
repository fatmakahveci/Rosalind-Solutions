#!/bin/env/python3.7

def dominant_probability(dom, het, rec):
	total = dom + het + rec

	return 1 - ((2 * 0.5 * (het * rec) / (total * (total - 1))) + (rec * (rec - 1)) / (total * (total - 1)) + (het * (het - 1)) / (total * (total - 1)) * 0.25)

if __name__ == '__main__':
	with open("rosalind.txt", 'r') as file:
		dom, het, rec = map(float, file.readline().split(' '))
		file.close()
	print("%.5f" % dominant_probability(dom, het, rec))
