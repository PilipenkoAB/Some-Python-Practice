# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 13:00:38 2019

@author: Pilipenko A B

code - merge sort
"""

#creating an array
item = [5, 4, 2, 9, 3, 11]

#merge sort function
def merge_sort(item):
    
    # if array consist of more than one element
    if len(item) > 1:
        middle = len(item) // 2     # Find middle of the array - // divide without "float"
        left = item[:middle]        # Put left side to the left array
        right = item[middle:]       # Put right side to the right array
        
        # recursion - repeat the devide action 
        merge_sort(left)
        merge_sort(right)
        
        #merging
        i = 0 #indext left array
        j = 0 #index right array
        k = 0 #index merged array
        
        #while both arrays have content
        while i <len(left) and j<len(right):
            if left[i] < right[j]:
                item[k] = left [i]
                i += 1
            else:
                item[k] = right[j]
                j += 1
            k += 1
        
        #if left array still has values, add item
        while i < len(left):
            print(1)
            item[k] = left[i]
            i += 1
            k += 1
        
        # if right array still has values, add item
        while j < len(right):
            print(2)
            item[k] = right[j]
            j += 1
            k += 1
    
    
    return item

#invoke merge sort function
result = merge_sort(item)

# print and result array
print(f"result - {result}")