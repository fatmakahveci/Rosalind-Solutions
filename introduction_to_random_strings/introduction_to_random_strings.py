#!/usr/bin/env/ python3.7

import math

if __name__=="__main__":

    with open("rosalind.txt", 'r') as file:
        seq = file.readline().strip() # seq := sequence
        gc_pr_list = list(map(float, file.readline().strip('\n').split(' ')))
        file.close()

    pr_list = [] # pr := probability
    n_gc = seq.count('G') + seq.count('C')
    n_at = len(seq) - n_gc
    for gc_pr in gc_pr_list: 
        prob = math.log10((((1 - gc_pr) / 2)**n_at) * (gc_pr / 2)**n_gc)
        pr_list.append('%0.3f' % prob)

    pr_list = map(str, pr_list)
    print(' '.join(pr_list))
