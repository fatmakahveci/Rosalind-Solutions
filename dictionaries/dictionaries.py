#!/bin/env/python

file_name='dictionaries.txt'
file_content=open(file_name,'r').read().split(' ')
a=set(file_content)
b = [file_content.count(e) for e in a]
a=list(a)
b=list(b)
for i in xrange(len(a)):
	print a[i]+' '+str(b[i])