## Why this benchmark?
Computation heavy workloads are especially problematic for interpretation. A typical example
of these kinds of workloads are matrix operations, such as matrix inversion.

## Performance Measurements

* python: `3.347s, 3.363s, 3.415s, 3.409s, 3.393s`
* cython, no modifications, only compiled: `2.010s, 2.036s, 2.019s, 2.035s, 2.010s`
* cython, add basic types (state of `matrix_invert_cython.pyx` before start of investigation): `1.591s, 1.645s, 1.619s, 1.644s, 1.621s`
* add `cpdef`s, `cdef`s, and some more remaining `int` types (state of `matrix_invert_cython_optim.pyx`): `1.440s, 1.439s, 1.440s, 1.483s, 1.444s`

 -> where is the speedup?

## Performance Measurements Detailed

### run
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
Total time: 2.4739 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
   102                                           cpdef run():
   103         1          2.0      2.0      0.0      cdef int n = 9
   104         1        275.0    275.0      0.0      A = create_matrix(n)
   105         1    2473458.0 2473458.0    100.0      A_inv = getMatrixInverse(A)
   106         1         74.0     74.0      0.0      res = mult(A, A_inv, n)
   107         1         45.0     45.0      0.0      res_int = mat_to_int(res)
   108                                               #print_matrix(res_int)
   109         1         51.0     51.0      0.0      print(check_ident(res_int))
```

Observations:
* `create_matrix` has roughly the same runtime independent from the way of execution (guess: same explanation as for heap_sort)
* `mult` receives a good speedup from compilation (investigation should be done in `matrix_mult/`), `mat_to_int` also, but less
* overall runtime is dominated by creating the actual inverse matrix

### getMatrixInverse
**Python**
```
Total time: 7.35097 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    70                                           def getMatrixInverse(m):
    71         1     734144.0 734144.0     10.0      determinant = getMatrixDeternminant(m)
    72                                               #special case for 2x2 matrix:
    73         1          2.0      2.0      0.0      if len(m) == 2:
    74                                                   return [[m[1][1]/determinant, -1*m[0][1]/determinant],
    75                                                           [-1*m[1][0]/determinant, m[0][0]/determinant]]
    76
    77                                               #find matrix of cofactors
    78         1          1.0      1.0      0.0      cofactors = []
    79        10          3.0      0.3      0.0      for r in range(len(m)):
    80         9          3.0      0.3      0.0          cofactorRow = []
    81        90         70.0      0.8      0.0          for c in range(len(m)):
    82        81        383.0      4.7      0.0              minor = getMatrixMinor(m,r,c)
    83        81    6616212.0  81681.6     90.0              cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
    84         9          7.0      0.8      0.0          cofactors.append(cofactorRow)
    85         1         13.0     13.0      0.0      cofactors = transposeMatrix(cofactors)
    86        10          5.0      0.5      0.0      for r in range(len(cofactors)):
    87        90         56.0      0.6      0.0          for c in range(len(cofactors)):
    88        81         75.0      0.9      0.0              cofactors[r][c] = cofactors[r][c]/determinant
    89         1          0.0      0.0      0.0      return cofactors
```

**Cython**
```
Total time: 3.52679 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    73                                           def getMatrixInverse(m):
    74         1     350151.0 350151.0      9.9      determinant = getMatrixDeternminant(m)
    75                                               #special case for 2x2 matrix:
    76         1          2.0      2.0      0.0      if len(m) == 2:
    77                                                   return [[m[1][1]/determinant, -1*m[0][1]/determinant],
    78                                                           [-1*m[1][0]/determinant, m[0][0]/determinant]]
    79
    80                                               #find matrix of cofactors
    81         1          1.0      1.0      0.0      cofactors = []
    82        10         78.0      7.8      0.0      for r in range(len(m)):
    83         9          2.0      0.2      0.0          cofactorRow = []
    84        90         92.0      1.0      0.0          for c in range(len(m)):
    85        81        274.0      3.4      0.0              minor = getMatrixMinor(m,r,c)
    86        81    3176110.0  39211.2     90.1              cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
    87         9          5.0      0.6      0.0          cofactors.append(cofactorRow)
    88         1         13.0     13.0      0.0      cofactors = transposeMatrix(cofactors)
    89        10          4.0      0.4      0.0      for r in range(len(cofactors)):
    90        90         22.0      0.2      0.0          for c in range(len(cofactors)):
    91        81         35.0      0.4      0.0              cofactors[r][c] = cofactors[r][c]/determinant
    92         1          1.0      1.0      0.0      return cofactors
```

**Cython - typed**
```
Total time: 2.80489 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    80                                           cpdef getMatrixInverse(m):
    81                                               cdef int c, r
    82         1     285495.0 285495.0     10.2      determinant = getMatrixDeternminant(m)
    83                                               #special case for 2x2 matrix:
    84         1          1.0      1.0      0.0      if len(m) == 2:
    85                                                   return [[m[1][1]/determinant, -1*m[0][1]/determinant],
    86                                                           [-1*m[1][0]/determinant, m[0][0]/determinant]]
    87
    88                                               #find matrix of cofactors
    89         1          0.0      0.0      0.0      cofactors = []
    90         1          1.0      1.0      0.0      for r in range(len(m)):
    91         9          1.0      0.1      0.0          cofactorRow = []
    92         9          6.0      0.7      0.0          for c in range(len(m)):
    93        81        239.0      3.0      0.0              minor = getMatrixMinor(m,r,c)
    94        81    2519087.0  31099.8     89.8              cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
    95         9         13.0      1.4      0.0          cofactors.append(cofactorRow)
    96         1         10.0     10.0      0.0      cofactors = transposeMatrix(cofactors)
    97         1          0.0      0.0      0.0      for r in range(len(cofactors)):
    98         9          3.0      0.3      0.0          for c in range(len(cofactors)):
    99        81         36.0      0.4      0.0              cofactors[r][c] = cofactors[r][c]/determinant
   100         1          1.0      1.0      0.0      return cofactors
```
