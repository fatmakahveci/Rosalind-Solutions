#!/bin/env/python

variables=open('rabbits_and_recurrence_relations.txt','r').read().split(' ')
nm_months=long(variables[0])
nm_offsprings=long(variables[1])

def number_of_rabbits(month,offspring):
	if month == 1 or month == 2:
		return 1
	return number_of_rabbits(month-1, offspring) + offspring * number_of_rabbits(month-2, offspring)

def main():
	print str(number_of_rabbits(nm_months,nm_offsprings))

if __name__ == '__main__':
	main()