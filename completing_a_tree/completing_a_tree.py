#!/bin/env/python

import operator

file_name='completing_a_tree.txt'


def main():
    file_content = open(file_name, 'r').read().split('\n')
    n=int(file_content[0])
    edges=list(sorted(file_content[1:],key=operator.itemgetter(2)))
    tree=list()
    cluster=set()
    for edge in edges:
        u=edge.split(' ')[0]
        v=edge.split(' ')[1]
        if u not in cluster and v not in cluster:
            cluster = set()
            tree.append(cluster)

        cluster.add(u)
        cluster.add(v)
    total_linked_elements=0
    for cl in tree:
        total_linked_elements+=len(cl)

    print(len(tree)-1+n-total_linked_elements)

if __name__=="__main__":
    main()