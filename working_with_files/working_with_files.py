#!/bin/env/python

if __name__ == "__main__":
    with open("rosalind.txt","r") as file:
    	for idx, line in enumerate(file, start=1):
        	if idx % 2 == 0:
        		print(line.strip())
