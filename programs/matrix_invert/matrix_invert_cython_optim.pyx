#!/usr/bin/env python3
# cython: language_level=3str
# cython: binding=True
# cython: linetrace=True
# distutils: define_macros=CYTHON_TRACE_NOGIL=1
import random
from cpython cimport bool

PROFILER="line_profiler"

cpdef create_matrix(int n, empty=False):
    cdef int i, j
    A = []
    for i in range(n):
        if empty:
            A.append([0] * n)
        else:
            line = []
            for j in range(n):
                line.append(random.randint(0, 10000))
            A.append(line)
    return A

cpdef bool check_ident(A):
    cdef int i, j
    for i in range(len(A)):
        for j in range(len(A[i])):
            if i == j and A[i][j] != 1:
                return False
            if i != j and A[i][j] != 0:
                return False
    return True

cpdef mat_to_int(A):
    cdef int i, j
    B = []
    for i in range(len(A)):
        B.append([])
        for j in range(len(A[i])):
            B[i].append(int(round(A[i][j], 0)))
            #A[i][j] = int(A[i][j])
    return B

# source: https://www.geeksforgeeks.org/python-program-multiply-two-matrices/
cpdef mult(A, B, int n):
    cdef int i, j, k
    result = create_matrix(n, empty=True)
    # iterating by row of A
    for i in range(len(A)):
        # iterating by column by B
        for j in range(len(B[0])):
            # iterating by rows of B
            for k in range(len(B)):
                 result[i][j] += A[i][k] * B[k][j]
    return result

cdef void print_matrix(A):
    print("======================================")
    for r in A:
        print(r)

# source: https://stackoverflow.com/a/39881366
cdef transposeMatrix(m):
    return list(map(list,zip(*m)))

cdef getMatrixMinor(m, int i, int j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

cdef getMatrixDeternminant(m):
    cdef int c
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    return determinant

cpdef getMatrixInverse(m):
    cdef int c, r
    determinant = getMatrixDeternminant(m)
    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)
    cofactors = transposeMatrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors

cpdef run():
    cdef int n = 9
    A = create_matrix(n)
    A_inv = getMatrixInverse(A)
    res = mult(A, A_inv, n)
    res_int = mat_to_int(res)
    #print_matrix(res_int)
    print(check_ident(res_int))

def run_wrapper():
    # line_profiler + cython is weird
    n = 6
    pass
