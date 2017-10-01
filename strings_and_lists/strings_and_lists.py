#!/bin/env/python

file_name='strings_and_lists.txt'

file_content=open(file_name,'r').read().split('\n')
text=file_content[0]
variables=file_content[1].split(' ')
a=int(variables[0])
b=int(variables[1])
c=int(variables[2])
d=int(variables[3])

print text[a:b+1] +' '+text[c:d+1]