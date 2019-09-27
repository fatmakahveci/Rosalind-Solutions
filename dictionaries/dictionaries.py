#!/bin/env/python

if __name__ == "__main__":

    file_content = open("rosalind.txt", 'r').read().split(' ')
    a = list(set(file_content))
    b = [file_content.count(e) for e in a]
    for i in range(len(a)):
        print(a[i] + ' ' + str(b[i]))
