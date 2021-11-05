#cython: language_level=3
import numpy as np

# Import compile time information about numpy: https://cython.readthedocs.io/en/latest/src/tutorial/numpy.html
cimport numpy as np

np.import_array()
DTYPE = np.float

ctypedef np.float_t DTYPE_t


def main():
    cdef int n = 10000
    cdef np.ndarray A = np.random.rand(n, n)
    cdef np.ndarray B = np.random.rand(n, n)
    cdef np.ndarray C = np.matmul(A, B)
    return
