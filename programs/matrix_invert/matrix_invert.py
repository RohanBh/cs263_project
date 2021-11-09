#!/usr/bin/env python3
import random

PROFILER="line_profiler"

def create_matrix(n, empty=False):
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

def check_ident(A):
    for i in range(len(A)):
        for j in range(len(A[i])):
            if i == j and A[i][j] != 1:
                return False
            if i != j and A[i][j] != 0:
                return False
    return True

def mat_to_int(A):
    B = []
    for i in range(len(A)):
        B.append([])
        for j in range(len(A[i])):
            B[i].append(int(round(A[i][j], 0)))
            #A[i][j] = int(A[i][j])
    return B

# source: https://www.geeksforgeeks.org/python-program-multiply-two-matrices/
def mult(A, B, n):
    result = create_matrix(n, empty=True)
    # iterating by row of A
    for i in range(len(A)):
        # iterating by column by B
        for j in range(len(B[0])):
            # iterating by rows of B
            for k in range(len(B)):
                 result[i][j] += A[i][k] * B[k][j]
    return result

def print_matrix(A):
    print("======================================")
    for r in A:
        print(r)

# source: https://stackoverflow.com/a/39881366
def transposeMatrix(m):
    return list(map(list,zip(*m)))

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeternminant(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    return determinant

def getMatrixInverse(m):
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

def run():
    n = 9
    A = create_matrix(n)
    A_inv = getMatrixInverse(A)
    res = mult(A, A_inv, n)
    res_int = mat_to_int(res)
    #print_matrix(res_int)
    print(check_ident(res_int))


import timeit
print(timeit.repeat(run, repeat=5, number=1))
"""
if PROFILER == "cProfile":
    import cProfile
    cProfile.run("run()", "matrix_invert_c.stats")
elif PROFILER == "line_profiler":
    # correct usage according to https://stackoverflow.com/a/43377717
    import line_profiler
    prof = line_profiler.LineProfiler()
    prof_wrapper = prof(run)
    prof_wrapper()
    """

#    n = 9
#    A = create_matrix(n)
#    prof_wrapper = prof(getMatrixInverse)
#    prof_wrapper(A)
"""

    prof.print_stats()
elif PROFILER == "profile":
    import profile
    profile.run("run()", "matrix_invert_p.stats")
else:
    import sys
    print("unknown profiler1")
    sys.exit(1)
"""
