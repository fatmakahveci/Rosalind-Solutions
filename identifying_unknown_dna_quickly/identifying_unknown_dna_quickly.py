#!/bin/env/python

file_name = 'identifying_unknown_dna_quickly.txt'


def main():
    file_content = open(file_name, 'r').read().split('\n')
    
    for line in file_content:
        print(line)


if __name__ == "__main__":
    main()

