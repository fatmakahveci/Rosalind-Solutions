#!/usr/bin/env python3.7


if __name__ == '__main__':
    with open("rosalind.txt", 'r') as file:
        N, x = map(float, file.readline().strip('\n').split(' '))
        seq = file.readline().strip('\n')
        file.close()
    n_at = seq.count('A') + seq.count('T')
    n_gc = len(seq) - n_at

    s_prob = (((1 - x) / 2) ** n_at) * (((x) / 2) ** n_gc)
    prob = 1 - (1 - s_prob) ** N
    print('%0.3f' % prob)
