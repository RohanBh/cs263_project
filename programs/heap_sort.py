#!/usr/bin/env python3
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
    n = len(arr)
    print ("Sorted array is")
    for i in range(n):
        print (arr[i],end=" ")
    print("")

# heapify
def heapify(arr, n, i):
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

if PROFILER == "cProfile":
    import cProfile
    cProfile.run("main()", "heap_sort_c.stats")
elif PROFILER == "line_profiler":
    # correct usage according to https://stackoverflow.com/a/43377717
    import line_profiler
    profiler = line_profiler.LineProfiler()
    profiler_wrapper = profiler(main)
    profiler_wrapper()
    profiler.print_stats()
elif PROFILER == "profile":
    import profile
    profile.run("main()", "heap_sort_p.stats")
else:
    import sys
    print("unknown profiler!")
    sys.exit(1)
