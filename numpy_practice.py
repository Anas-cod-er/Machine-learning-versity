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




# print(newarr)


#join

arr4 = nm.array([[0,9],[8,7]])
arr5 = nm.array([[4,5],[4,7]])

arr6 = nm.concatenate((arr4,arr5),axis=1)
# print(arr6)


arr7 =nm.array([6,7,9])
arr8 = nm.array([0,5,2])

arr9 = nm.hstack((arr7,arr8))

# print(arr9)

arr10 = nm.array([1, 2, 3, 4, 5, 4, 4])

x = nm.where(arr10 == 4)
y = nm.where(arr10 %2 ==1)

# print(y)


arr11 = nm.array([3, 2, 0, 1])

print(nm.sort(arr11))





