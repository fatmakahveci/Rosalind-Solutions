#!/usr/bin/env python3.7


if __name__ == "__main__":
    with open("rosalind.txt", 'r') as file:
        n, k = map(int, file.readline().strip('\n').split(' '))
        file.close()

    permutation = 1
    for i in range(k):
        permutation *= (n - i)
    print(permutation % 1000000)
