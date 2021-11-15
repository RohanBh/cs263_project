## Why this benchmark?
Interpretation is problematic for computation-heavy workloads. HeapSort is a CPU-bound algorithm
but has a different memory access pattern and different operations than typical matrix operations.

## Performance Measurements overall

* python: `1.487s, 1.490s, 1.532s, 1.568s, 1.536s`
* cython, no types added: `1.065s, 0.921s, 0.917s, 0.929s, 0.930s`
* cython, add types only to heapify (current state of `heap_sort_cython.pyx`): `0.518s, 0.525s, 0.525s, 0.520s, 0.535s`
* add as many types as possible, including return types (see `heap_sort_cython_optim.pyx`): `0.192s, 0.195s, 0.184s, 0.191s, 0.187s`
-> there is a speedup, why?

## Performance detailed

### Main

**Python**
```
Total time: 5.86377 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    51                                           def main():
    52         1          1.0      1.0      0.0      n = 200000
    53         1     601397.0 601397.0     10.3      arr = create_array(n)
    54         1    5262367.0 5262367.0     89.7      heapSort(arr)
    55         1          1.0      1.0      0.0      if PRINT:
    56                                                   print_array(arr)
```

**Cython**
```
Total time: 1.29225 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     9                                           def wrapper():
    10         1          1.0      1.0      0.0      n = 200000
    11         1     553456.0 553456.0     42.8      arr = heap_sort_cython.create_array(n)
    12         1     738790.0 738790.0     57.2      heap_sort_cython.heapSort(arr)
```

**Cython - typed**
```
Total time: 0.610609 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     9                                           def wrapper():
    10         1     610609.0 610609.0    100.0      heap_sort_cython_optim.main()

```

**Cython, using cpdef insted of cdef**
```
Total time: 0.603051 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     9                                           def wrapper():
    10         1          1.0      1.0      0.0      n = 200000
    11         1     542983.0 542983.0     90.0      arr = heap_sort_cython_optim.create_array(n)
    12         1      60067.0  60067.0     10.0      heap_sort_cython_optim.heapSort(arr)
    13                                               #heap_sort_cython_optim.main()
```

* biggest speedup in `heapSort`
* some speedup in `create_array`, but `heapSort` is more interesting

### HeapSort()

**Python**
```
Total time: 5.43806 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    40                                           def heapSort(arr):
    41         1          6.0      6.0      0.0      n = len(arr)
    42                                               # maxheap
    43    200002      54126.0      0.3      1.0      for i in range(n, -1, -1):
    44    200001     464998.0      2.3      8.6          heapify(arr, n, i)
    45                                               # element extraction
    46    200000      64669.0      0.3      1.2      for i in range(n-1, 0, -1):
    47    199999      78670.0      0.4      1.4          arr[i], arr[0] = arr[0], arr[i] # swap
    48    199999    4775594.0     23.9     87.8          heapify(arr, i, 0)
```

**Cython**
```
Total time: 3.40874 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    62                                           def heapSort(arr):
    63         1          2.0      2.0      0.0      n = len(arr)
    64                                               # maxheap
    65    200002      42123.0      0.2      1.2      for i in range(n, -1, -1):
    66    200001     311725.0      1.6      9.1          heapify(arr, n, i)
    67                                               # element extraction
    68    200000      51293.0      0.3      1.5      for i in range(n-1, 0, -1):
    69    199999      51979.0      0.3      1.5          arr[i], arr[0] = arr[0], arr[i] # swap
    70    199999    2951620.0     14.8     86.6          heapify(arr, i, 0)
```

*Note*: to make tracing of the cythonized function possible, additional flags for the cython compiler need to be set. This seems to be the reason for the slower execution time. Even though, the relative timings showing where execution is spend should be similar to the distribution of the previous profiling.

**Cython - typed**
```
Total time: 1.82712 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    49                                           cpdef void heapSort(int[:] arr):
    50                                               cdef int n, i
    51         1          1.0      1.0      0.0      n = len(arr)
    52                                               # maxheap
    53         1          0.0      0.0      0.0      for i in range(n, -1, -1):
    54    200001     181091.0      0.9      9.9          heapify(arr, n, i)
    55                                               # element extraction
    56         1          0.0      0.0      0.0      for i in range(n-1, 0, -1):
    57    199999      47372.0      0.2      2.6          arr[i], arr[0] = arr[0], arr[i] # swap
    58    199999    1598659.0      8.0     87.5          heapify(arr, i, 0)
```

*Note*: see above

 * most time is spent in heapify
 * there is also the biggest speedup
 * the array swap is in the cythonized version faster than in python

### heapify()

* looking at `heap_sort_cython_optim.html` and `heap_sort_cython.html` show that the amount of interactions with python are drastically reduced
* especially `heapify` and `heapSort` differ

**Python**
```
Total time: 7.5e-05 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    23                                           def heapify(arr, n, i):
    24        18          8.0      0.4     10.7      largest = i # largest value
    25        18          5.0      0.3      6.7      l = 2 * i + 1 # left
    26        18         11.0      0.6     14.7      r = 2 * i + 2 # right
    27                                               # if left child exists
    28        18          5.0      0.3      6.7      if l < n and arr[i] < arr[l]:
    29        17          8.0      0.5     10.7          largest = l
    30                                               # if right child exits
    31        18          6.0      0.3      8.0      if r < n and arr[largest] < arr[r]:
    32        10          4.0      0.4      5.3          largest = r
    33                                               # root
    34        18          5.0      0.3      6.7      if largest != i:
    35        17          8.0      0.5     10.7          arr[i],arr[largest] = arr[largest],arr[i] # swap
    36                                                   # root.
    37        17         15.0      0.9     20.0          heapify(arr, n, largest)
```

**Cython**
```
Total time: 4.8e-05 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    29                                           def heapify(arr, n, i):
    30        18          9.0      0.5     18.8      largest = i # largest value
    31        18          3.0      0.2      6.2      l = 2 * i + 1 # left
    32        18          3.0      0.2      6.2      r = 2 * i + 2 # right
    33                                               # if left child exists
    34        18          4.0      0.2      8.3      if l < n and arr[i] < arr[l]:
    35        17          2.0      0.1      4.2          largest = l
    36                                               # if right child exits
    37        18          8.0      0.4     16.7      if r < n and arr[largest] < arr[r]:
    38         5          2.0      0.4      4.2          largest = r
    39                                               # root
    40        18          3.0      0.2      6.2      if largest != i:
    41        17          6.0      0.4     12.5          arr[i],arr[largest] = arr[largest],arr[i] # swap
    42                                                   # root.
    43        17          8.0      0.5     16.7          heapify(arr, n, largest)
```

**Cython - Typed**
```
Total time: 2.7e-05 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    31                                           cpdef void heapify(int[:] arr, int n, int i):
    32                                               cdef int largest, l, r
    33        18          2.0      0.1      7.4      largest = i # largest value
    34        18          2.0      0.1      7.4      l = 2 * i + 1 # left
    35        18          2.0      0.1      7.4      r = 2 * i + 2 # right
    36                                               # if left child exists
    37        18          4.0      0.2     14.8      if l < n and arr[i] < arr[l]:
    38        17          2.0      0.1      7.4          largest = l
    39                                               # if right child exits
    40        18          1.0      0.1      3.7      if r < n and arr[largest] < arr[r]:
    41         6          1.0      0.2      3.7          largest = r
    42                                               # root
    43        18          3.0      0.2     11.1      if largest != i:
    44        17          4.0      0.2     14.8          arr[i],arr[largest] = arr[largest],arr[i] # swap
    45                                                   # root.
    46        17          6.0      0.4     22.2          heapify(arr, n, largest)
```

* comparing the execution times of all the lines in the cython-typed example shows that the pure cython lines are in general faster than the ones with python interaction (except from the function call, but that's no surprise)
* primitive types don't need python interactions, if all elements of an interaction are primitive
* (normal, non numpy) arrays need bound checks -> pythoninteraction in the error case -> still faster, but not as fast as primitive types

Speedup from compilation to typed compilation by line:
 30 - 33  5x            \
 31 - 34  2x            |
 32 - 35  2x            |
 34 - 37  1x            |
 35 - 38  1x             \ on average 2.125
 37 - 40  4x             / 
 38 - 41  2x            |
 40 - 43  1x            |
 41 - 44  2x            |
 43 - 46  1.25x         /

* for all lines of speedup, the amount of interaction with python decreased
* the first three, 38-41 have no interaction at all anymore
* 37-40, 41-44 has mostly c instructions (especially compared to the non-typed version), python interaction only for errors
(can all be seen by looking at the html files)


## Conclusions
* operations with primitive types only lead to a huge speedup
* arrays when annotated are also complete C, but modeled by structs to enable boundary checking
* if boundary checking fails, python interaction for the error
* the checks lead to some overhead compared to c arrays (not measured)
