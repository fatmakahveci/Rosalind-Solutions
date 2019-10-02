#!/usr/bin/env python3.7


if __name__ == '__main__':
    with open("rosalind.txt", 'r') as file:
        N = int(file.readline().strip('\n'))
        seq = file.readline().strip('\n')
        A = map(float, file.readline().strip('\n').split(' '))
        file.close()

    n_gc = seq.count('G') + seq.count('C')
    n_at = seq.count('A') + seq.count('T')

    B = []
    for pr in A:
        P = (((1 - pr) / 2) ** n_at) * ((pr / 2) ** n_gc) * (N - len(seq) + 1)
        B.append('%.3f' % P)
    print(' '.join(B))
