## Performance Measurements

#### Python version
```
Timer unit: 1e-06 s

Total time: 5.95635 s
File: heap_sort.py
Function: main at line 51

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    51                                           def main():
    52         1          2.0      2.0      0.0      n = 200000
    53         1     608204.0 608204.0     10.2      arr = create_array(n)
    54         1    5348143.0 5348143.0     89.8      heapSort(arr)
    55         1          2.0      2.0      0.0      if PRINT:
    56                                                   print_array(arr)
```

#### Cython versions

* no modifications, only compiled


```language
Timer unit: 1e-06 s

Total time: 1.28147 s
File: profile_heap_cython.pyx
Function: wrapper at line 9

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     9                                           def wrapper():
    10         1          2.0      2.0      0.0      n = 200000
    11         1     552613.0 552613.0     43.1      arr = heap_sort_cython.create_array(n)
    12         1     728851.0 728851.0     56.9      heap_sort_cython.heapSort(arr)

```

* add types only to heapify: `def heapify(arr, int n, int i`, `cdef int largest, l, r` (current state of `heap_sort_cython.pyx`)

```
Timer unit: 1e-06 s

Total time: 0.955532 s
File: profile_heap_cython.pyx
Function: wrapper at line 9

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     9                                           def wrapper():
    10         1          4.0      4.0      0.0      n = 200000
    11         1     569137.0 569137.0     59.6      arr = heap_sort_cython.create_array(n)
    12         1     386391.0 386391.0     40.4      heap_sort_cython.heapSort(arr)
```

* add as many types as possible, including return types (see `heap_sort_cython_optim.pyx`)

```
Timer unit: 1e-06 s

Total time: 0.621139 s
File: profile_heap_cython_optim.pyx
Function: wrapper at line 9

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     9                                           def wrapper():
    10         1     621137.0 621137.0    100.0      heap_sort_cython_optim.main()
    11         1          2.0      2.0      0.0      return
    12                                               n = 200000
    13                                               arr = heap_sort_cython.create_array(n)
    14                                               heap_sort_cython.heapSort(arr)
```