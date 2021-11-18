#cython: language_level=3
from cpython cimport array
import array


def sieve(_n):
    cdef int n = _n
    # https://cython.readthedocs.io/en/latest/src/tutorial/array.html#safe-usage-with-memory-views
    cdef array.array a = array.array('i', [1] * (n + 1))
    cdef int[:] arr = a
    # i -- smallest prime so far
    cdef int i = 2
    # http://docs.cython.org/en/latest/src/userguide/pyrex_differences.html#automatic-range-conversion
    # for loops are optimized because j is typed
    cdef int j, found
    while i <= n:
        for j in range(2*i, n+1, i):
            arr[j] = 0
        found = 0
        for j in range(i+1, n+1, 1):
            if arr[j] == 1:
                i = j
                found = 1
                break
        if found == 0:
            break

    return


def main():
    sieve(2000000)
    return
