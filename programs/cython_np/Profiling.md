# Profiling Numpy operations
In this experiment, we call numpy to generate random matrices and also to multiply two matrices. As numpy is already implemented in C, using cython shouldn't make much difference in performance.

## Python
Running `timeit`: 5.36s
Times (in seconds): `[5.2628198098391294, 4.541318390984088, 4.502866978989914, 4.470005344133824, 4.474340090993792]`
Median (in seconds): `4.502866978989914`

## Cython
Running `timeit`: 5.42s
Times (in seconds): `[5.4998264538589865, 4.639143645064905, 4.985978234093636, 4.464157968992367, 4.496893273899332]`
Median (in seconds): `4.639143645064905`

## Cython type-optimized
Running `timeit`: 5.32s
Times (in seconds): `[5.488181414082646, 4.841542878188193, 4.526103527983651, 4.500269568990916, 4.488695902051404]`
Median (in seconds): `4.526103527983651`

# Conclusion
We get almost comparable performance for Python and Cython when using numpy operations
