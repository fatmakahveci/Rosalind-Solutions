#!/bin/env/python

from collections import deque

input_file = "aho_corasick.txt"

adjacency_list = []


def create_trie(keywords):
    create_empty_trie()
    add_keywords(keywords)
    put_fail_transitions()


def create_empty_trie():
    root = {'value': '', 'next_states': [], 'fail_state': 0, 'output': []}
    adjacency_list.append(root)


def add_keywords(keywords):
    for keyword in keywords:
        add_keyword(keyword)


def add_keyword(keyword):
    current_state = 0
    j = 0

    keyword = keyword.lower()  # just in case

    child = find_next_state(current_state, keyword[j])
    while child != None:  # loop: i.e. to add "crowd" after "cash"
        current_state = child
        j += 1
        if j < len(keyword):
            child = find_next_state(current_state, keyword[j])
        else:
            break

    for i in range(j, len(keyword)):  # loop: add remaining keyword until the end
        node = {'value': keyword[i], 'next_states': [], 'fail_state': 0, 'output': []}
        adjacency_list.append(node)
        adjacency_list[current_state]['next_states'].append(len(adjacency_list) - 1)
        current_state = len(adjacency_list) - 1
    adjacency_list[current_state]['output'].append(keyword)  # to add whole keyword at the end


def find_next_state(current_state, value):
    for node in adjacency_list[current_state]['next_states']:
        if adjacency_list[node]['value'] == value:
            return node
    return None


def put_fail_transitions():
    q = deque()

    for node in adjacency_list[0]['next_states']:
        q.append(node)

    while q:
        r = q.popleft()  # to remove and return the leftmost side
        for child in adjacency_list[r]['next_states']:
            q.append(child)
            state = adjacency_list[r]['fail_state']

            while find_next_state(state, adjacency_list[child]['value']) == None and state != 0:
                state = adjacency_list[state]['fail_state']

            adjacency_list[child]['fail_state'] = find_next_state(state, adjacency_list[child]['value'])
            if find_next_state(state, adjacency_list[child]['value']) == None:
                adjacency_list[child]['fail_state'] = 0
            # print(find_next_state(state, adjacency_list[child]['value']))

            adjacency_list[child]['output'] += adjacency_list[adjacency_list[child]['fail_state']]['output']

    print('----------------------------------------------------------------------')
    print('Build tree')
    print('----------------------------------------------------------------------')
    for element in adjacency_list:
        print('char:',element['value'],'next states:',element['next_states'],'fail state:',element['fail_state'],'output:',element['output'])

def get_found_keywords(text):
    text = text.lower()

    found_keywords = []

    current_state = 0
    for i in range(len(text)):
        while find_next_state(current_state, text[i]) is None and current_state != 0:
            current_state = adjacency_list[current_state]['fail_state']
        current_state = find_next_state(current_state, text[i])
        if current_state is None:
            current_state = 0
        for j in adjacency_list[current_state]['output']:
            found_keywords.append({'index': i - len(j) + 1, 'word': j})
    return found_keywords


def main():
    file_content = open(input_file, 'r').read().split('\n')

    keywords = list(file_content[0].strip().split())
    text = file_content[1].strip()

    create_trie(keywords)
    found_keywords=get_found_keywords(text)
    print('----------------------------------------------------------------------')
    print('Search')
    print('----------------------------------------------------------------------')
    for found_keyword in found_keywords:
        print('keyword:',found_keyword['word'],'index:',found_keyword['index'])
    print('----------------------------------------------------------------------')

if __name__ == "__main__":
    main()
