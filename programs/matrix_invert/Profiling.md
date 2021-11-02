## Performance Measurements

#### Pure Python
```
Timer unit: 1e-06 s

Total time: 7.28344 s
File: matrix_invert.py
Function: run at line 91

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    91                                           def run():
    92         1          1.0      1.0      0.0      n = 9
    93         1        274.0    274.0      0.0      A = create_matrix(n)
    94         1    7282668.0 7282668.0    100.0      A_inv = getMatrixInverse(A)
    95         1        358.0    358.0      0.0      res = mult(A, A_inv, n)
    96         1         79.0     79.0      0.0      res_int = mat_to_int(res)
    97                                               #print_matrix(res_int)
    98         1         60.0     60.0      0.0      print(check_ident(res_int))
```

#### Cython

* no modifications, only compiled

```
Timer unit: 1e-06 s

Total time: 2.03589 s
File: profile_matrix_invert_cython.py
Function: wrapper at line 9

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     9                                           def wrapper():
    10         1          3.0      3.0      0.0      n = 9
    11         1        247.0    247.0      0.0      A = matrix_invert_cython.create_matrix(n)
    12         1    2035447.0 2035447.0    100.0      A_inv = matrix_invert_cython.getMatrixInverse(A)
    13         1         55.0     55.0      0.0      res = matrix_invert_cython.mult(A, A_inv, n)
    14         1         76.0     76.0      0.0      res_int = matrix_invert_cython.mat_to_int(res)
    15         1         62.0     62.0      0.0      print(matrix_invert_cython.check_ident(res_int))
```

* add a few int types for loop indices except from `getMatrixInverse` and `getMatrixDeterminant`, add int type for arg of `create_matrix`

```
Timer unit: 1e-06 s

Total time: 1.98174 s
File: profile_matrix_invert_cython.py
Function: wrapper at line 9

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     9                                           def wrapper():
    10         1          1.0      1.0      0.0      n = 9
    11         1        240.0    240.0      0.0      A = matrix_invert_cython.create_matrix(n)
    12         1    1981390.0 1981390.0    100.0      A_inv = matrix_invert_cython.getMatrixInverse(A)
    13         1         43.0     43.0      0.0      res = matrix_invert_cython.mult(A, A_inv, n)
    14         1         41.0     41.0      0.0      res_int = matrix_invert_cython.mat_to_int(res)
    15         1         23.0     23.0      0.0      print(matrix_invert_cython.check_ident(res_int))
```

* add types to remaining loop indices

```
Timer unit: 1e-06 s

Total time: 1.58075 s
File: profile_matrix_invert_cython.py
Function: wrapper at line 9

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     9                                           def wrapper():
    10         1          1.0      1.0      0.0      n = 9
    11         1        247.0    247.0      0.0      A = matrix_invert_cython.create_matrix(n)
    12         1    1580392.0 1580392.0    100.0      A_inv = matrix_invert_cython.getMatrixInverse(A)
    13         1         49.0     49.0      0.0      res = matrix_invert_cython.mult(A, A_inv, n)
    14         1         37.0     37.0      0.0      res_int = matrix_invert_cython.mat_to_int(res)
    15         1         24.0     24.0      0.0      print(matrix_invert_cython.check_ident(res_int))
```

* numpy version not tested: it is not possible, to do this automatically, since I had to reproduce python array manipulations for numpyarrays

* add `cpdef` and some more remaining `int` types (state of `matrix_invert_cython_optim.pyx`)

```
Timer unit: 1e-06 s

Total time: 1.80834 s
File: profile_matrix_invert_cython_optim.py
Function: wrapper at line 9

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     9                                           def wrapper():
    10         1          1.0      1.0      0.0      n = 9
    11         1        253.0    253.0      0.0      A = matrix_invert_cython_optim.create_matrix(n)
    12         1    1807969.0 1807969.0    100.0      A_inv = matrix_invert_cython_optim.getMatrixInverse(A)
    13         1         48.0     48.0      0.0      res = matrix_invert_cython_optim.mult(A, A_inv, n)
    14         1         43.0     43.0      0.0      res_int = matrix_invert_cython_optim.mat_to_int(res)
    15         1         25.0     25.0      0.0      print(matrix_invert_cython_optim.check_ident(res_int))
```