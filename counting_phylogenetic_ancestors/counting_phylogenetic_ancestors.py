#!/bin/env/python

file_name = 'counting_phylogenetic_ancestors.txt'


def main():
    n = int(open(file_name, 'r').read().strip())
    print(n - 2)


if __name__ == "__main__":
    main()
