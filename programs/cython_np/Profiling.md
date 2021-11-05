# Profiling Numpy operations
In this experiment, we call numpy to generate random matrices and also to multiply two matrices. As numpy is already implemented in C, using cython shouldn't make much difference in performance.

## Python
Running `timeit`: 5.36s

## Cython
Running `timeit`: 5.42s

## Cython type-optimized
Running `timeit`: 5.32s

# Conclusion
We get almost comparable performance for Python and Cython when using numpy operations
