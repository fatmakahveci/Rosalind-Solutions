#!/bin/env/python

file_name='conditions_and_loops.txt'

variables=open(file_name,'r').read().split(' ')
a=int(variables[0])
b=int(variables[1])

ans=0
for num in xrange(a,b):
	if num%2==1:
		ans+=num
print ans