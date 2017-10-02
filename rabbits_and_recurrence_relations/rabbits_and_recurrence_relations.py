#!/bin/env/python

file_name = 'rabbits_and_recurrence_relations.txt'

variables = open(file_name, 'r').read().split(' ')
nm_months = int(variables[0])
nm_offsprings = int(variables[1])


def number_of_rabbits(month, offspring):
    if month == 1 or month == 2:
        return 1
    return number_of_rabbits(month - 1, offspring) + offspring * number_of_rabbits(month - 2, offspring)


def main():
    print(str(number_of_rabbits(nm_months, nm_offsprings)))


if __name__ == '__main__':
    main()
