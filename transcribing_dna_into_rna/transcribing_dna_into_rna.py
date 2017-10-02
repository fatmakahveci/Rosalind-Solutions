#!/bin/env/python

import sys

file_name = 'transcribing_dna_into_rna.txt'


def main():
    file_content = open(file_name, 'r').read()

    for i in range(len(file_content)):
        if file_content[i] == 'T':
            sys.stdout.write("U")
        else:
            sys.stdout.write(file_content[i])
    print("")


if __name__ == "__main__":
    main()
