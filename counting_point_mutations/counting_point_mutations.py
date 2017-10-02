#!/bin/env/python

file_name = 'counting_point_mutations.txt'


def readfile():
    return open(file_name, 'r').read()


def get_sequences():
    seq_list = []
    for i in range(2):
        seq_list.append(readfile().split('\n')[i])
    return seq_list


def calculate_point_mutations():
    seq_list = get_sequences()
    num_pt_mut = 0
    for i in range(len(seq_list[0])):
        if seq_list[0][i] != seq_list[1][i]:
            num_pt_mut += 1
    return num_pt_mut


def main():
    print(str(calculate_point_mutations()))


if __name__ == '__main__':
    main()

