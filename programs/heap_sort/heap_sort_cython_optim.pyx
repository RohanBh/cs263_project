#!/usr/bin/env python3
# cython: profile=True
# cython: language_level=3str
import random
from cpython cimport array
import array

PROFILER = "profile"
PRINT = False


cdef int[:] create_array(int n):
    cdef int[:] arr = array.array('i', [0] * n)
    cdef int i
    for i in range(n):
        arr[i] = (random.randint(0,20000))
    return arr

# source adapted from https://www.tutorialspoint.com/python-program-for-heap-sort
def print_array(arr):
    pass
    """
    n = len(arr)
    print ("Sorted array is")
    for i in range(n):
        print (arr[i],end=" ")
    print("")
    """

# heapify
cdef void heapify(int[:] arr, int n, int i):
    cdef int largest, l, r
    largest = i # largest value
    l = 2 * i + 1 # left
    r = 2 * i + 2 # right
    # if left child exists
    if l < n and arr[i] < arr[l]:
        largest = l
    # if right child exits
    if r < n and arr[largest] < arr[r]:
        largest = r
    # root
    if largest != i:
        arr[i],arr[largest] = arr[largest],arr[i] # swap
        # root.
        heapify(arr, n, largest)

# sort
cdef void heapSort(int[:] arr):
    cdef int n, i
    n = len(arr)
    # maxheap
    for i in range(n, -1, -1):
        heapify(arr, n, i)
    # element extraction
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i] # swap
        heapify(arr, i, 0)

# main
def main():
    cdef int n
    cdef int[:] arr
    n = 200000
    arr = create_array(n)
    heapSort(arr)
    if PRINT:
        print_array(arr)
