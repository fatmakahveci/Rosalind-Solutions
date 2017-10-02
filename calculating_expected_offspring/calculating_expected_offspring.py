#!/bin/env python

file_name = 'calculating_expected_offspring.txt'


def get_sequences(file_name):
    return open(file_name, 'r').read().split(' ')


def calculating_expected_offspring(file_name):
    genotype_list = map(float, get_sequences(file_name))

    return 2 * (
    genotype_list[0] + genotype_list[1] + genotype_list[2] + genotype_list[3] * 3 / 4 + genotype_list[4] / 2)


def main():
    print(str(calculating_expected_offspring(file_name)))


if __name__ == '__main__':
    main()
