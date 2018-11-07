#!/bin/env/python

import collections

file_name = 'find_the_longest_repeat_in_a_string.txt'


def construct_suffix_array(string, n):
    suffix_array_list = {'$': ''}

    for i in range(n):
        suffix_array_list[string[i:n]] = i
    return suffix_array_list


def longest_common_prefix(s, t):
    n = min(len(s), len(t))
    prefix = ""
    for i in range(n):
        if s[i] is t[i]:
            prefix += s[i]
        else:
            break
    return prefix


def main():
    string = open(file_name, 'r').read()
    n = len(string)

    suffix_array = list(collections.OrderedDict(sorted(construct_suffix_array(string, n).items())).keys())
    option_list = []
    for i in range(1, n):
        option_list.append(longest_common_prefix(suffix_array[i], suffix_array[i - 1]))

    lcp = ""
    for option in option_list:
        if len(lcp) < len(option):
            lcp = option
    print(lcp)


if __name__ == "__main__":
    main()
