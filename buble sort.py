# -*- coding: utf-8 -*
"""
Created on Thu Dec 12 11:39:38 2019

@author: Pilipenko A B

code - buble sort
"""

#creating an array
item = [3, 2, 1, 5, 9, 7, 6, 0, 12, 6, 29, 101, 4]

# buble sort function
def buble_sort(item):
    for i in range(len(item)-1,0,-1):
        for j in range(i):
            if item[j] > item[j+1]:
                temp = item[j]
                item[j] = item[j+1]
                item[j+1] = temp
                print(f"array {j} : {item}")
    return item

#invoke buble sort function
result = buble_sort(item)

# print start array and result array
print(f"      Result : {result}")