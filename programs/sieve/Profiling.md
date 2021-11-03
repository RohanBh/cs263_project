# Profiling Sieve of Eratosthenes
We call sieve to find prime numbers up to 20M.

## Python
Running `timeit`: 4.069404850248247

Running `line_profiler` on `main_wrapper` (at the highest level of function call)
```
Timer unit: 1e-06 s

Total time: 23.2114 s
File: /mnt/hdd/Projects/cs263_project/programs/sieve/sieve_of_eratosthenes.py
Function: main_wrapper at line 29

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    29                                           def main_wrapper():
    30         1   23211368.0 23211368.0    100.0      main()
    31         1          1.0      1.0      0.0      return
```

Running `line_profiler` on `sieve` directly.
```
Timer unit: 1e-06 s

Total time: 48.1729 s
File: /mnt/hdd/Projects/cs263_project/programs/sieve/sieve_of_eratosthenes.py
Function: sieve at line 1

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     1                                           def sieve(n=100):
     2         1    1196313.0 1196313.0      2.5      arr = [True for _ in range(n+1)]
     3                                               # i -- smallest prime so far
     4         1          1.0      1.0      0.0      i = 2
     5   1270607     327202.0      0.3      0.7      while i <= n:
     6  61128033   16091267.0      0.3     33.4          for j in range(2*i, n+1, i):
     7  59857426   18274306.0      0.3     37.9              arr[j] = False
     8   1270607     321939.0      0.3      0.7          found = False
     9  19999999    5469138.0      0.3     11.4          for j in range(i+1, n+1, 1):
    10  19999998    5219804.0      0.3     10.8              if arr[j]:
    11   1270606     318766.0      0.3      0.7                  i = j
    12   1270606     320424.0      0.3      0.7                  found = True
    13   1270606     319832.0      0.3      0.7                  break
    14   1270607     313930.0      0.2      0.7          if not found:
    15         1          1.0      1.0      0.0              break
    16
    17                                               # for i in range(2, n+1):
    18                                               #     if arr[i]:
    19                                               #         print(i)
    20                                               # print('Total primes:')
    21                                               # print(len([1 for x in arr if x]) - 2)
    22         1          0.0      0.0      0.0      return
```

## Cython
Running `timeit`: 3.199113440234214

Running `line_profiler` on `main_wrapper` 
```
Timer unit: 1e-06 s

Total time: 3.18674 s
File: /mnt/hdd/Projects/cs263_project/programs/sieve/time_sieve.py
Function: main_wrapper at line 12

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    12                                           def main_wrapper():
    13         1    3186735.0 3186735.0    100.0      main()
    14         1          1.0      1.0      0.0      return
```

Running `line_profiler` on `sieve` directly. To build, run `python optim_cython_setup.py build_ext --inplace`.
```
Timer unit: 1e-06 s

Total time: 29.2323 s
File: sieve_of_eratosthenes_cython.pyx
Function: sieve at line 3

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     3                                           def sieve(n=100):
     4         1     204003.0 204003.0      0.7      arr = [True for _ in range(n+1)]
     5                                               # i -- smallest prime so far
     6         1          1.0      1.0      0.0      i = 2
     7         1          1.0      1.0      0.0      while i <= n:
     8  61128033   10030640.0      0.2     34.3          for j in range(2*i, n+1, i):
     9  59857426   11548496.0      0.2     39.5              arr[j] = False
    10   1270607     184987.0      0.1      0.6          found = False
    11  19999999    3351346.0      0.2     11.5          for j in range(i+1, n+1, 1):
    12  19999998    3110833.0      0.2     10.6              if arr[j]:
    13   1270606     193424.0      0.2      0.7                  i = j
    14   1270606     185154.0      0.1      0.6                  found = True
    15   1270606     192682.0      0.2      0.7                  break
    16   1270607     200418.0      0.2      0.7          if not found:
    17         1          1.0      1.0      0.0              break
    18         1      30342.0  30342.0      0.1      return
```

## Cython Optimized (with types)
Running `timeit`: 1.3275476680137217

Running `line_profiler` on `main_wrapper` 
```
Timer unit: 1e-06 s

Total time: 1.30329 s
File: /mnt/hdd/Projects/cs263_project/programs/sieve/time_optim_sieve.py
Function: main_wrapper at line 12

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    12                                           def main_wrapper():
    13         1    1303290.0 1303290.0    100.0      main()
    14         1          1.0      1.0      0.0      return
```
Running `line_profiler` on `sieve` directly (had to convert `cdef void sieve` to `def sieve`). To build, run: `python optim_cython_setup.py build_ext --inplace`
```
Timer unit: 1e-06 s

Total time: 24.012 s
File: sieve_of_eratosthenes_optim_cython.pyx
Function: sieve at line 6

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     6                                           def sieve(int n):
     7                                               # https://cython.readthedocs.io/en/latest/src/tutorial/array.html#safe-usage-with-memory-views
     8         1     450637.0 450637.0      1.9      cdef array.array a = array.array('i', [1] * (n + 1))
     9         1         12.0     12.0      0.0      cdef int[:] arr = a
    10                                               # i -- smallest prime so far
    11         1          0.0      0.0      0.0      cdef int i = 2
    12                                               # http://docs.cython.org/en/latest/src/userguide/pyrex_differences.html#automatic-range-conversion
    13                                               # for loops are optimized because j is typed
    14                                               cdef int j
    15         1          0.0      0.0      0.0      while i <= n:
    16  61128033   10051628.0      0.2     41.9          for j in range(2*i, n+1, i):
    17  59857426    9320432.0      0.2     38.8              arr[j] = 0
    18   1270607     193480.0      0.2      0.8          found = 0
    19   1270607     193932.0      0.2      0.8          for j in range(i+1, n+1, 1):
    20  19999998    3033266.0      0.2     12.6              if arr[j] == 1:
    21   1270606     190242.0      0.1      0.8                  i = j
    22   1270606     189778.0      0.1      0.8                  found = 1
    23   1270606     194389.0      0.2      0.8                  break
    24   1270607     190754.0      0.2      0.8          if found == 0:
    25         1          0.0      0.0      0.0              break
    26
    27         1       3446.0   3446.0      0.0      return
```


# Conclusion
Somehow, running `line_profiler` improves the cython performance but makes the python performance much worse.
