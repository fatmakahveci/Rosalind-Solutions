#!/bin/env/python

def read_file(file_name):
	return open(file_name,'r').read()

def get_variables(file_name):
	return map(long, read_file(file_name).split(' '))

def survivor_rabbits(month,survival_time):
	fibonacci_series=[0]*month
	for i in xrange(month):
		if i == 0 or i == 1:
			fibonacci_series[i]=1
		elif i < survival_time:
			fibonacci_series[i]=fibonacci_series[i-1]+fibonacci_series[i-2]
		elif i == survival_time:
			fibonacci_series[i]=fibonacci_series[i-1]+fibonacci_series[i-2]-1
		else:
			fibonacci_series[i]=fibonacci_series[i-1]+fibonacci_series[i-2]-fibonacci_series[i-survival_time-1]
	return fibonacci_series[month-1]

def mortal_fibonacci_rabbits(file_name):
	variables=get_variables(file_name)
	n=variables[0]
	m=variables[1]
	return survivor_rabbits(n,m)

def main():
	print str(mortal_fibonacci_rabbits('mortal_fibonacci_rabbits.txt'))

if __name__ == '__main__':
	main()