## Why this benchmark?
Computation heavy workloads are especially problematic for interpretation. A typical example
of these kinds of workloads are matrix operations, such as matrix inversion.

## Performance Measurements

* python: `3.347s, 3.363s, 3.415s, 3.409s, 3.393s`
* cython, no modifications, only compiled: `2.010s, 2.036s, 2.019s, 2.035s, 2.010s`
* cython, add basic types (state of `matrix_invert_cython.pyx` before start of investigation): `1.591s, 1.645s, 1.619s, 1.644s, 1.621s`
* add `cpdef` and some more remaining `int` types (state of `matrix_invert_cython_optim.pyx`): `1.581s, 1.595s, 1.588s, 1.600s, 1.607s`

 -> where is the speedup?

## Performance Measurements Detailed

**Python**
```
Total time: 7.40633 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    91                                           def run():
    92         1          2.0      2.0      0.0      n = 9
    93         1        273.0    273.0      0.0      A = create_matrix(n)
    94         1    7405554.0 7405554.0    100.0      A_inv = getMatrixInverse(A)
    95         1        366.0    366.0      0.0      res = mult(A, A_inv, n)
    96         1         78.0     78.0      0.0      res_int = mat_to_int(res)
    97                                               #print_matrix(res_int)
    98         1         61.0     61.0      0.0      print(check_ident(res_int))
```

**Cython**
```
Total time: 3.45128 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    94                                           def run():
    95         1          1.0      1.0      0.0      n = 9
    96         1        291.0    291.0      0.0      A = create_matrix(n)
    97         1    3450786.0 3450786.0    100.0      A_inv = getMatrixInverse(A)
    98         1         98.0     98.0      0.0      res = mult(A, A_inv, n)
    99         1         48.0     48.0      0.0      res_int = mat_to_int(res)
   100                                               #print_matrix(res_int)
   101         1         53.0     53.0      0.0      print(check_ident(res_int))
```

**Cython - typed**
*Note*: Matrices are a problem for cython type annotation, since there is no matrix type other than numpy arrays. The conversion between operations on python list matrices and numpy matrices is not trivial -> we are limited to using python lists
```
Total time: 2.95927 s
File: matrix_invert_cython_optim.pyx
Function: run at line 102

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
   102                                           def run():
   103         1          1.0      1.0      0.0      cdef int n = 9
   104         1        243.0    243.0      0.0      A = create_matrix(n)
   105         1    2958831.0 2958831.0    100.0      A_inv = getMatrixInverse(A)
   106         1         92.0     92.0      0.0      res = mult(A, A_inv, n)
   107         1         49.0     49.0      0.0      res_int = mat_to_int(res)
   108                                               #print_matrix(res_int)
   109         1         52.0     52.0      0.0      print(check_ident(res_int))
```
```
Total time: 2.4739 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
   102                                           def run():
   103         1          2.0      2.0      0.0      cdef int n = 9
   104         1        275.0    275.0      0.0      A = create_matrix(n)
   105         1    2473458.0 2473458.0    100.0      A_inv = getMatrixInverse(A)
   106         1         74.0     74.0      0.0      res = mult(A, A_inv, n)
   107         1         45.0     45.0      0.0      res_int = mat_to_int(res)
   108                                               #print_matrix(res_int)
   109         1         51.0     51.0      0.0      print(check_ident(res_int))
```
