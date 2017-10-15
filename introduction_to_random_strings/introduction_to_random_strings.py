#!/bin/env/python

import math

file_name='introduction_to_random_strings.txt'

def main():
    file_content=open(file_name,'r').read().split('\n')

    sequence=file_content[0]
    gc_contents=list(map(float,file_content[1].strip().split(' ')))

    for gc_content in gc_contents:
        probability = 0.0
        for base in sequence:
            if base == 'G' or base == 'C':
                probability+=math.log(gc_content/2.0,10)
            else:
                probability+=math.log((1.0-gc_content)/2.0,10)

        print('{0: 0.3f}'.format(probability))

if __name__=="__main__":
    main()