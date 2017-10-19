#!/bin/env/python

from itertools import count

file_name = 'introduction_to_pattern_matching.txt'


class Trie(object):
    def __init__(self):
        self.counter = count(start=1)
        self.root = [next(self.counter), {}]

def write_result(parent):
    parents_child = parent[1]
    parents_parent = parent[0]
    for character, child in parents_child.items():
        childs_parent = child[0]
        print(parents_parent, childs_parent, character)
        write_result(child)


def main():
    strings = list(open(file_name, 'r').read().split('\n'))
    trie = Trie()
    for string in strings:
        node = trie.root
        for character in string:
            nodes_child = node[1]
            if character not in nodes_child:
                nodes_child[character] = [next(trie.counter), {}]
            node = nodes_child[character]

    write_result(trie.root)


if __name__ == '__main__':
    main()
