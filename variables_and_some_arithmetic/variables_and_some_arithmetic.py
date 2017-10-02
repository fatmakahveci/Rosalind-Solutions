#!/bin/env/python

file_name = 'variables_and_some_arithmetic.txt'


def main():
    variables = open(file_name, 'r').read().split(' ')
    a = float(variables[0])
    b = float(variables[1])
    print(str(int(a * a + b * b)))


if __name__ == "__main__":
    main()
