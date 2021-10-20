#!/usr/bin/env python3
# cython: profile=True
# cython: language_level=3str
import random

PROFILER = "profile"
PRINT = False


def create_array(n):
    arr = []
    for i in range(n):
        arr.append(random.randint(0,20000))
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
def heapify(arr, int n, int i):
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

def heapify_base(arr, n, i):
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
        heapify_base(arr, n, largest)

# sort
def heapSort(arr):
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
    n = 200000
    arr = create_array(n)
    heapSort(arr)
    if PRINT:
        print_array(arr)
