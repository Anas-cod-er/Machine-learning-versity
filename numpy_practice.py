import numpy as nm

arr = nm.array([1, 2, 3, 4, 5])

# 2d array
arr2 = nm.array([[2, 3, 5, 7,9], [0, 1, 1, 0,11]])

# print('5th element on 2nd row: ', arr2[1, 4])

#slice
# print(arr[1:5])

# print(arr[-3:-1])


#reshape
arr3 = nm.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

newarr = arr3.reshape(4, 3)

print(newarr)

