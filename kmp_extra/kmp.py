#!/bin/env/python

from Bio import SeqIO
from io import StringIO

file_name = 'kmp.txt'


def failure_function(pattern):
    m = len(pattern)
    failure = [0] * m
    i = 1
    j = 0
    
    while i < m:
        if pattern[i] == pattern[j]:
            failure[i] = j + 1
            i += 1
            j += 1
        elif j > 0:
            j = failure[j - 1]
        else:
            failure[i] = 0
            i += 1
    return failure


def kmp(text, pattern):
    F = failure_function(pattern)
    print('Failure function: ' + str(F))
    i = 0
    j = 0
    n = len(text)
    m = len(pattern)
    while i < n:
        if text[i] == pattern[j]:
            if j == (m - 1):
                return i - j
            else:
                i += 1
                j += 1
        else:
            if j > 0:
                j = F[j - 1]
            else:
                i += 1
        print(str(i) + ' ' + str(j))
    return -1


def main():
    text = list(SeqIO.parse(StringIO(open(file_name, 'r').read()), 'fasta'))[0].seq
    pattern = list(SeqIO.parse(StringIO(open(file_name, 'r').read()), 'fasta'))[1].seq
    index = kmp(text, pattern)
    print('Index: ' + str(index))
    print('Matching text: ' + text[index:index + len(pattern)])


if __name__ == '__main__':
    main()

