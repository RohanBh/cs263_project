#cython: language_level=3

cdef void sieve(int n=100):
    cdef int arr[200000]
    arr[:] = [1 for _ in range(200000)]
    # i -- smallest prime so far
    cdef int i = 2
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
    sieve(200000)
    return
