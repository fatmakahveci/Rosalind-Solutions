#!/bin/env/python

file_name = 'conditions_and_loops.txt'


def main():
    variables = open(file_name, 'r').read().split(' ')
    a = int(variables[0])
    b = int(variables[1])

    ans = 0
    for num in range(a, b):
        if num % 2 == 1:
            ans += num
    print(ans)


if __name__ == "__main__":
    main()
