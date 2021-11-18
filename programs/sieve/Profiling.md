# Profiling Sieve of Eratosthenes
We call sieve to find prime numbers up to `2M`.

## Wny?
Sieve of eratosthenes is a program that finds prime numbers up to a particular number by eliminating all the factors of primes found so far. The program execution time is dominated by looping and indexing overheads as opposed to compute overheads (eg in `matrix_invert` or `cython_np`)

## Python
```
Timer unit: 1e-06 s

Total time: 5.7788 s
File: /home/rohan/projects/cs263_project/programs/sieve/sieve_of_eratosthenes.py
Function: sieve at line 1

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     1                                           def sieve(n=100):
     2         1     168179.0 168179.0      2.9      arr = [True for _ in range(n+1)]
     3                                               # i -- smallest prime so far
     4         1          1.0      1.0      0.0      i = 2
     5    148933      49979.0      0.3      0.9      while i <= n:
     6   5808800    1936401.0      0.3     33.5          for j in range(2*i, n+1, i):
     7   5659867    2000535.0      0.4     34.6              arr[j] = False
     8    148933      48417.0      0.3      0.8          found = False
     9   1999999     704879.0      0.4     12.2          for j in range(i+1, n+1, 1):
    10   1999998     673544.0      0.3     11.7              if arr[j]:
    11    148932      48024.0      0.3      0.8                  i = j
    12    148932      50914.0      0.3      0.9                  found = True
    13    148932      49136.0      0.3      0.9                  break
    14    148933      48793.0      0.3      0.8          if not found:
    15         1          1.0      1.0      0.0              break
    16
    17                                               # for i in range(2, n+1):
    18                                               #     if arr[i]:
    19                                               #         print(i)
    20                                               # print('Total primes:')
    21                                               # print(len([1 for x in arr if x]) - 2)
    22         1          1.0      1.0      0.0      return

Total time: 11.2081 s
File: /home/rohan/projects/cs263_project/programs/sieve/sieve_of_eratosthenes.py
Function: main at line 25

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    25                                           def main():
    26         1   11208082.0 11208082.0    100.0      sieve(2000000)
    27         1          1.0      1.0      0.0      return
```

## Cython
```
Timer unit: 1e-06 s

Total time: 3.53637 s
File: sieve_of_eratosthenes_cython.pyx
Function: sieve at line 3

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     3                                           def sieve(n=100):
     4         1      28755.0  28755.0      0.8      arr = [True for _ in range(n+1)]
     5                                               # i -- smallest prime so far
     6         1          1.0      1.0      0.0      i = 2
     7         1          1.0      1.0      0.0      while i <= n:
     8   5808800    1243457.0      0.2     35.2          for j in range(2*i, n+1, i):
     9   5659867    1245373.0      0.2     35.2              arr[j] = False
    10    148933      29386.0      0.2      0.8          found = False
    11   1999999     450836.0      0.2     12.7          for j in range(i+1, n+1, 1):
    12   1999998     413659.0      0.2     11.7              if arr[j]:
    13    148932      30241.0      0.2      0.9                  i = j
    14    148932      29472.0      0.2      0.8                  found = True
    15    148932      30131.0      0.2      0.9                  break
    16    148933      31428.0      0.2      0.9          if not found:
    17         1          1.0      1.0      0.0              break
    18         1       3630.0   3630.0      0.1      return

Total time: 6.72896 s
File: sieve_of_eratosthenes_cython.pyx
Function: main at line 21

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    21                                           def main():
    22         1    6728954.0 6728954.0    100.0      sieve(2000000)
    23         1          1.0      1.0      0.0      return
```

## Cython Optimized (with types)
```
Timer unit: 1e-06 s

Total time: 2.9767 s
File: sieve_of_eratosthenes_cython_typed.pyx
Function: sieve at line 6

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     6                                           def sieve(_n):
     7         1          1.0      1.0      0.0      cdef int n = _n
     8                                               # https://cython.readthedocs.io/en/latest/src/tutorial/array.html#safe-usage-with-memory-views
     9         1      63043.0  63043.0      2.1      cdef array.array a = array.array('i', [1] * (n + 1))
    10         1         15.0     15.0      0.0      cdef int[:] arr = a
    11                                               # i -- smallest prime so far
    12         1          0.0      0.0      0.0      cdef int i = 2
    13                                               # http://docs.cython.org/en/latest/src/userguide/pyrex_differences.html#automatic-range-conversion
    14                                               # for loops are optimized because j is typed
    15                                               cdef int j, found
    16         1          0.0      0.0      0.0      while i <= n:
    17                                                   # for j in range(2*i, n+1, i):
    18                                                   # for j from 2*i <= j < n+1 by i:
    19    148933      29323.0      0.2      1.0          j = 2 * i
    20    148933      29912.0      0.2      1.0          while j < n + 1:
    21   5659867    1153262.0      0.2     38.7              arr[j] = 0
    22   5659867    1120965.0      0.2     37.7              j += i
    23    148933      31237.0      0.2      1.0          found = 0
    24    148933      29778.0      0.2      1.0          for j in range(i+1, n+1, 1):
    25   1999998     400384.0      0.2     13.5              if arr[j] == 1:
    26    148932      29763.0      0.2      1.0                  i = j
    27    148932      29344.0      0.2      1.0                  found = 1
    28    148932      29605.0      0.2      1.0                  break
    29    148933      29732.0      0.2      1.0          if found == 0:
    30         1          0.0      0.0      0.0              break
    31
    32         1        336.0    336.0      0.0      return

Total time: 5.82451 s
File: sieve_of_eratosthenes_cython_typed.pyx
Function: main at line 35

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    35                                           def main():
    36         1    5824507.0 5824507.0    100.0      sieve(2000000)
    37         1          0.0      0.0      0.0      return

```

Timer outputs:
```
# Python
Times: [0.4172210490796715, 0.40910623292438686, 0.40258224005810916, 0.4040722558274865, 0.4026290869805962]
Median: 0.4040722558274865
# Cython
Times: [0.2820059529040009, 0.2711405160371214, 0.26613495498895645, 0.2662159700412303, 0.264668351970613]
Median: 0.2662159700412303
# Cython typed
Times: [0.09256194299086928, 0.0762948680203408, 0.0704366760328412, 0.0706046090926975, 0.07054292690008879]
Median: 0.0706046090926975
```
