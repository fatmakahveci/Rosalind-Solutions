#!/bin/env/python

import math

file_name = 'binary_search.txt'


def binary_search(sorted_list, key, n):
    first_index = 0
    last_index = len(sorted_list) - 1
    is_found = False
    while first_index <= last_index and not is_found:
        middle_index = math.floor((first_index + last_index) / 2)
        if sorted_list[middle_index] == key:
            is_found = True
        elif key < sorted_list[middle_index]:
            last_index = middle_index - 1
        else:
            first_index = middle_index + 1
    if is_found:
        return str(middle_index + 1)
    else:
        return str(-1)


def main():
    file_content = list(open(file_name, 'r').read().strip().split('\n'))

    n, m = int(file_content[0]), int(file_content[1])

    sorted_list = list(map(int, file_content[2].split(' ')))
    key_list = list(map(int, file_content[3].split(' ')))

    index_list = []
    for key in key_list:
        index_list.append(binary_search(sorted_list, key, n))

    print(' '.join(index_list))


if __name__ == '__main__':
    main()
