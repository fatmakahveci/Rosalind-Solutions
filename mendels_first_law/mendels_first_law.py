#!/bin/env/python

file_name='mendels_first_law.txt'

variable_list=[]

def readfile():
	return open(file_name,'r').read()

def get_variables():
	for i in xrange(len(readfile().split(' '))):
		variable_list.append(float(readfile().split(' ')[i]))
	return variable_list

def main():
	dom=get_variables()[0]
	het=get_variables()[1]
	rec=get_variables()[2]
	total=dom+het+rec

	result = 1 - ((2*0.5*(het*rec)/(total*(total-1))) + (rec*(rec-1))/(total*(total-1)) + (het*(het-1))/(total*(total-1))*0.25)

	print("%.5f" % result)

if __name__ == '__main__':
	main()