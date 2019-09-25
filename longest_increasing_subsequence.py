# Longest Increasing Subsequence

if __name__ == "__main__":


    def longest_increasing_subsequence(array, n):
        longest_increasing_subsequence_list = []
        
        length_array = [1] * n
        subseq_array = [0] * n

        for i in range(len(array)):
            j = 0
            for j in range(i):
                if array[i] > array[j] and length_array[j] + 1 >= length_array[i]:
                    length_array[i] = length_array[j] + 1
                    subseq_array[i] = j

        max_element_index = length_array.index(max(length_array))
        i = max_element_index
        while True:
            longest_increasing_subsequence_list.append(array[i])
            i = subseq_array[i]
            if i == 0:
                break
        return longest_increasing_subsequence_list[::-1]

    with open("a.txt", "r") as file:
        n = int(file.readline().strip())
        lds_array = map(int, file.readline().strip().split(' '))
        
        file.close()
        
        print(' '.join(map(str,longest_increasing_subsequence(lds_array, n))))
        print(' '.join(map(str,longest_increasing_subsequence(lds_array[::-1], n)[::-1])))
