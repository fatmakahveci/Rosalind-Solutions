#!/bin/env/python

import collections

file_name = 'construct_the_suffix_array_of_a_string.txt'


def main():
    string = open(file_name, 'r').read()
    suffix_array_list = {'$': ''}
    n = len(string)
    for i in range(n):
        suffix_array_list[string[i:n]] = i
    values = list(collections.OrderedDict(sorted(suffix_array_list.items())).values())

    for i in range(n):
        if i != n-1:
            print(str(values[i]) + ', ', end='')
        else:
            print(str(values[i]), end='')


if __name__ == "__main__":
    main()
