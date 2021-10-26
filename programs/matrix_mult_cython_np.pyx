# cython: profile=True
# cython: language_level=3str
import random
import numpy as np

# modified version of: https://www.geeksforgeeks.org/python-program-multiply-two-matrices/

DTYPE = np.intc

# Program to multiply two matrices using nested loops
def create_matrix_typed(int n, empty=False):
    cdef Py_ssize_t i, j
    A = np.zeros((n,n))
    cdef Py_ssize_t length = n
    if not empty:
        for i in range(length):
            for j in range(length):
                A[i][j] = (random.randint(0, 10000))
    return A

def create_matrix(n, empty=False):
    A = np.zeros((n,n))
    if not empty:
        for i in range(n):
            for j in range(n):
                A[i][j] = (random.randint(0, 10000))
    return A

def mult(A, B, n):
    return A * B
    """
    result = create_matrix(n, empty=True)
    # iterating by row of A
    for i in range(len(A)):
        # iterating by column by B
        for j in range(len(B[0])):
            # iterating by rows of B
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result
    """

def print_matrix(A):
    print("=================================================")
    for r in A:
        print(r)

def run():
    n = 200
    A = create_matrix(n)
    print_matrix(A)
    B = create_matrix(n)
    print_matrix(B)

    result = mult(A, B, n)
    print_matrix(result)
