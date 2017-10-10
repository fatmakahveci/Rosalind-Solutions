#!/bin/env/python

from collections import defaultdict

file_name = "introduction_to_pattern_matching.txt"


def main():
    strings = list(open(file_name, 'r').read().split('\n'))
    trie=defaultdict(list)
    char_index=2

    for string in strings:
        start_index=1
        for char in string:
            if char not in trie[start_index]:
                trie[start_index].append(char)
                if char not in trie[start_index-1]:
                    print(str(start_index)+' ' + str(char_index) + ' ' + char)
                else:
                    print(str(char_index-1) + ' ' + str(char_index) + ' ' + char)
                char_index += 1
            start_index+=1

if __name__ == "__main__":
    main()
