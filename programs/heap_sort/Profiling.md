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
 * the array swap is in the cythonized version faster than in python ( **TODO** check whether this line is pure c)
