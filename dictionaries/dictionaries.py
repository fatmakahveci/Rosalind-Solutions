#!/bin/env/python

file_name = 'dictionaries.txt'


def main():
    file_content = open(file_name, 'r').read().split(' ')
    a = set(file_content)
    b = [file_content.count(e) for e in a]
    a = list(a)
    b = list(b)
    for i in range(len(a)):
        print(a[i] + ' ' + str(b[i]))


if __name__ == "__main__":
    main()
