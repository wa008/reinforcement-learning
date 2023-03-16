'''
    print ('\r') can make cursor back to the front of line, can't make curcos back last few lines
    print of python can't display dynamic map
'''
import sys 
import time
import random

arr = []
cnt = 40
for i in range(cnt):
    arr.append(['*' for i in range(cnt)])

def print_arr(arr):
    for ar in arr:
        for val in ar:
            print (val, end = '')
        print ('')

arr[cnt // 2][cnt // 2] = '-'
def move(arr):
    flag = False
    for i in range(len(arr)):
        ar = arr[i]
        for j in range(len(ar)):
            if arr[i][j] == '-':
                arr[i][j] = ''
                num = random.randint(0, 4)
                if num == 0:
                    arr[i + 1][j] = '-'
                elif num == 1:
                    arr[i - 1][j] = '-'
                elif num == 2:
                    arr[i][j + 1] = '-'
                else:
                    arr[i][j - 1] = '-'
                flag = True 
                break
        if flag == True:
            break 
    return arr 

print_arr(arr)
for i in range(100):
    arr = move(arr)
    print_arr(arr)
    time.sleep(0.3)
    print ('-' * cnt)
