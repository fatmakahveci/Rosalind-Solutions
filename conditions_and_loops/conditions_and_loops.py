#!/bin/env/python

if __name__ == "__main__":
    a,b = map(int, open('rosalind.txt', 'r').readline().split(' '))
    print(sum(list(filter(lambda x: x % 2 == 1, range(a, b)))))
