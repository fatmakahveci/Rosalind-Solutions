#!/bin/env/python

file_name = 'fibonacci_numbers.txt'


def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


def main():
    n = int(open(file_name, 'r').read().strip())
    print(fibonacci(n))


if __name__ == '__main__':
    main()
