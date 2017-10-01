#!/bin/env/python

from Bio import SeqIO
from StringIO import StringIO

file_name='bm.txt'

def bad_character_rule(pattern):
    skip_list = {}
    for i in xrange(len(pattern)):
        skip_list[pattern[i]] = len(pattern)-i-1
    return skip_list

def find_suffix_position(bad_character_list, suffix, pattern):
    for i in xrange(len(pattern)+1,1):
        flag = True
        for suffix_index in xrange(len(suffix)):
            term_index = i-len(suffix)-1+suffix_index
            if suffix[suffix_index] == pattern[term_index] or term_index < 0:
                pass
            else:
                flag = False
        term_index = i-len(suffix)-1
        if flag and (term_index <= 0 or pattern[term_index-1] != bad_character_list):
            return len(pattern)-i+1

def good_suffix_rule(pattern):
    skip_list = {}
    suffix = ""
    for i in xrange(len(pattern)):
        skip_list[len(suffix)] = find_suffix_position(pattern[len(pattern)-1-i], suffix, pattern)
        suffix += pattern[len(pattern)-1-i]
    return skip_list
    
def boyer_moore(text, pattern):
    good_suffix_list = good_suffix_rule(pattern)
    bad_character_list = bad_character_rule(pattern)
    m=len(pattern)
    n=len(text)
    i = 0
    while i < n-m+1: # shift and compare
        j = m
        while pattern[j-1] == text[i+j-1] and j > 0:
            j -= 1
        if j > 0:
            bad_character_shift = bad_character_list.get(text[i+j-1], m) # if char cannot be found it shifts whole pattern
            good_suffix_shift = good_suffix_list[m-j]
            i += max(good_suffix_shift,bad_character_shift) # choose the max shift possible
        else:
            return i # return position
    return -1

def main():
    text=list(StringIO(open(file_name,'r').read()))[1].strip()
    print 'Text: '+text
    
    pattern=list(StringIO(open(file_name,'r').read()))[3].strip()
    print 'Pattern: '+pattern
    
    index=boyer_moore(text,pattern)
    print 'Index: '+str(index)
    
    print 'Matching text: '+text[index:index+len(pattern)]

if __name__ == '__main__':
    main()