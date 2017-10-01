#!/bin/env/python

file_name='working_with_files.txt'

with open(file_name,'r') as file:
	num=0
	for line in file:
		num+=1
		if num%2==0:
			print line.strip()