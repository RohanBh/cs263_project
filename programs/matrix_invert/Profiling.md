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

Observations:
 * The source lines containing `getMatrixDeternminant` dominate the execution.
 * For loops with typed index variables are considerably faster than interpreted or non-typed for loops.

### getMatrixDeternminant

**Python**
```
Total time: 0.934999 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    60                                           def getMatrixDeternminant(m):
    61                                               #base case for 2x2 matrix
    62    260650      99620.0      0.4     10.7      if len(m) == 2:
    63    181440      99160.0      0.5     10.6          return m[0][0]*m[1][1]-m[0][1]*m[1][0]
    64
    65     79210      22594.0      0.3      2.4      determinant = 0
    66    339859     119673.0      0.4     12.8      for c in range(len(m)):
    67    260649     573150.0      2.2     61.3          determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    68     79210      20802.0      0.3      2.2      return determinant
```
```
Total time: 1.17212 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    60                                           def getMatrixDeternminant(m):
    61                                               #base case for 2x2 matrix
    62    260650      87830.0      0.3      7.5      if len(m) == 2:
    63    181440     100289.0      0.6      8.6          return m[0][0]*m[1][1]-m[0][1]*m[1][0]
    64
    65     79210      21690.0      0.3      1.9      determinant = 0
    66    339859     116312.0      0.3      9.9      for c in range(len(m)):
    67    260649     496587.0      1.9     42.4          new_det = getMatrixMinor(m, 0, c)
    68    260649      95716.0      0.4      8.2          new_det = getMatrixDeternminant(new_det)
    69    260649     144843.0      0.6     12.4          new_det = ((-1)**c)*m[0][c]*new_det
    70    260649      87094.0      0.3      7.4          determinant += new_det
    71                                                   #determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    72     79210      21758.0      0.3      1.9      return determinant
```
```
Total time: 4.94184 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    60                                           def getMatrixDeternminant(m):
    61                                               #base case for 2x2 matrix
    62    260650     362415.0      1.4      7.3      if len(m) == 2:
    63    181440     415638.0      2.3      8.4          return m[0][0]*m[1][1]-m[0][1]*m[1][0]
    64
    65     79210      91531.0      1.2      1.9      determinant = 0
    66    339859     484194.0      1.4      9.8      for c in range(len(m)):
    67    260649    2137007.0      8.2     43.2          new_det = getMatrixMinor(m, 0, c)
    68    260649     378257.0      1.5      7.7          new_det = getMatrixDeternminant(new_det)
    69    260649     613011.0      2.4     12.4          new_det = ((-1)**c)*m[0][c]*new_det
    70    260649     369351.0      1.4      7.5          determinant += new_det
    71                                                   #determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    72     79210      90434.0      1.1      1.8      return determinant
```

**Cython**
```
Total time: 0.485324 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    63                                           def getMatrixDeternminant(m):
    64                                               #base case for 2x2 matrix
    65    260650      54102.0      0.2     11.1      if len(m) == 2:
    66    181440      47693.0      0.3      9.8          return m[0][0]*m[1][1]-m[0][1]*m[1][0]
    67
    68     79210      15945.0      0.2      3.3      determinant = 0
    69    339859      85170.0      0.3     17.5      for c in range(len(m)):
    70    260649     266318.0      1.0     54.9          determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    71     79210      16096.0      0.2      3.3      return determinant
```
```
Total time: 0.665994 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    63                                           def getMatrixDeternminant(m):
    64                                               #base case for 2x2 matrix
    65    260650      52610.0      0.2      7.9      if len(m) == 2:
    66    181440      47384.0      0.3      7.1          return m[0][0]*m[1][1]-m[0][1]*m[1][0]
    67
    68     79210      15878.0      0.2      2.4      determinant = 0
    69    339859      82162.0      0.2     12.3      for c in range(len(m)):
    70    260649     213598.0      0.8     32.1          new_det = getMatrixMinor(m, 0, c)
    71    260649      70543.0      0.3     10.6          new_det = getMatrixDeternminant(new_det)
    72    260649     106224.0      0.4     15.9          new_det = ((-1)**c)*m[0][c]*new_det
    73    260649      61637.0      0.2      9.3          determinant += new_det
    74                                                   #determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    75     79210      15958.0      0.2      2.4      return determinant
```
```
Total time: 2.7933 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    63                                           def getMatrixDeternminant(m):
    64                                               #base case for 2x2 matrix
    65    260650     224742.0      0.9      8.0      if len(m) == 2:
    66    181440     202865.0      1.1      7.3          return m[0][0]*m[1][1]-m[0][1]*m[1][0]
    67
    68     79210      66456.0      0.8      2.4      determinant = 0
    69    339859     346661.0      1.0     12.4      for c in range(len(m)):
    70    260649     895609.0      3.4     32.1          new_det = getMatrixMinor(m, 0, c)
    71    260649     284278.0      1.1     10.2          new_det = getMatrixDeternminant(new_det)
    72    260649     442562.0      1.7     15.8          new_det = ((-1)**c)*m[0][c]*new_det
    73    260649     261575.0      1.0      9.4          determinant += new_det
    74                                                   #determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    75     79210      68552.0      0.9      2.5      return determinant
```

**Cython - typed**
```
Total time: 0.348921 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    69                                           cpdef getMatrixDeternminant(m):
    70                                               cdef int c
    71                                               #base case for 2x2 matrix
    72    260650      48746.0      0.2     14.0      if len(m) == 2:
    73    181440      44884.0      0.2     12.9          return m[0][0]*m[1][1]-m[0][1]*m[1][0]
    74
    75     79210      14194.0      0.2      4.1      determinant = 0
    76     79210      14595.0      0.2      4.2      for c in range(len(m)):
    77    260649     210435.0      0.8     60.3          determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    78     79210      16067.0      0.2      4.6      return determinant
```
```
Total time: 0.509395 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    69                                           cpdef getMatrixDeternminant(m):
    70                                               cdef int c
    71                                               #base case for 2x2 matrix
    72    260650      48041.0      0.2      9.4      if len(m) == 2:
    73    181440      43758.0      0.2      8.6          return m[0][0]*m[1][1]-m[0][1]*m[1][0]
    74
    75     79210      14086.0      0.2      2.8      determinant = 0
    76     79210      14376.0      0.2      2.8      for c in range(len(m)):
    77    260649     188730.0      0.7     37.0          new_det = getMatrixMinor(m, 0, c)
    78    260649      58144.0      0.2     11.4          new_det = getMatrixDeternminant(new_det)
    79    260649      70405.0      0.3     13.8          new_det = ((-1)**c)*m[0][c]*new_det
    80    260649      57194.0      0.2     11.2          determinant += new_det
    81                                                   #determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    82     79210      14661.0      0.2      2.9      return determinant
```
```
Total time: 2.15487 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    69                                           cpdef getMatrixDeternminant(m):
    70                                               cdef int c
    71                                               #base case for 2x2 matrix
    72    260650     202619.0      0.8      9.4      if len(m) == 2:
    73    181440     185902.0      1.0      8.6          return m[0][0]*m[1][1]-m[0][1]*m[1][0]
    74
    75     79210      59329.0      0.7      2.8      determinant = 0
    76     79210      63074.0      0.8      2.9      for c in range(len(m)):
    77    260649     802188.0      3.1     37.2          new_det = getMatrixMinor(m, 0, c)
    78    260649     246025.0      0.9     11.4          new_det = getMatrixDeternminant(new_det)
    79    260649     291575.0      1.1     13.5          new_det = ((-1)**c)*m[0][c]*new_det
    80    260649     241998.0      0.9     11.2          determinant += new_det
    81                                                   #determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    82     79210      62163.0      0.8      2.9      return determinant
 ```

Observations:
 * Profiling is strange: why do I get 2 completely different results on the same machine???
 * The two last lines in the for-loop are exactly the same (look at html), but one of the lines has a different execution time between typed and non-typed (only in the new measurements)
 * defining a function as cpdef helps to reduce the LOC for calling the function quite a bitquite a bit (look at html)
 * (Are decref and incref GC functions?)
* `getMatrixMinor` contributes a good amount of the runtime (but similar between typed and nontyped)

### getMatrixMinor
**Differences between typed and non-typed**
 * Body nearly the same, only the calls to `_Pyx_PyInt_AddObjC` are missing from the typed version (the reason has to be the typed variables)
 * Prolog and epilog are completely different (one is python, huge init effort, other is C, only a few LOC)

## Conclusion
 * whenever possible define functions as `cdef` or atleast as `cpdef` (reduces calloverhead and prolog and epilog)
 * define type of the iterator in a for-loop
