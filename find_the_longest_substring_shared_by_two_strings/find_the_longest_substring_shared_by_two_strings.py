#!/bin/env/python

import collections

file_name = 'find_the_longest_substring_shared_by_two_strings.txt'


def construct_suffix_array(string, n):
    suffix_array_list = {'$': ''}

    for i in range(n):
        suffix_array_list[string[i:n]] = i
    return suffix_array_list


def longest_common_prefix_options(s, t):
    n = min(len(s), len(t))
    prefix = ""
    for i in range(n):
        if s[i] is t[i]:
            prefix += s[i]
        else:
            break
    return prefix


def longest_common_prefix(option_list):
    lcp = ""
    for option in option_list:
        if len(lcp) < len(option):
            lcp = option
    return lcp


def main():
    strings = open(file_name, 'r').read().split('\n')
    s = strings[0].strip()
    t = strings[1].strip()
    n, m = len(s), len(t)

    suffix_array_s = list(collections.OrderedDict(sorted(construct_suffix_array(s, n).items())).keys())
    suffix_array_t = list(collections.OrderedDict(sorted(construct_suffix_array(s, n).items())).keys())

    option_list = []
    for i in range(1, n):
        option = longest_common_prefix_options(suffix_array[i], suffix_array[i - 1])
        print(option)
        if '#' in option:
            option_list.append(option)

    lcp = longest_common_prefix(option_list)
    print(lcp)


if __name__ == "__main__":
    main()
