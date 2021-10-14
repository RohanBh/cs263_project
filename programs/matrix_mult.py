#!/usr/bin/env python3
import random
import cProfile
# modified version of: https://www.geeksforgeeks.org/python-program-multiply-two-matrices/

# Program to multiply two matrices using nested loops

# take a 3x3 matrix
A = [[12, 7, 3],
    [4, 5, 6],
    [7, 8, 9]]

# take a 3x4 matrix
B = [[5, 8, 1, 2],
    [6, 7, 3, 0],
    [4, 5, 9, 1]]


def create_matrix(n, empty=False):
    A = []
    for i in range(n):
        line = []
        for j in range(n):
            if empty:
                line.append(0)
            else:
                line.append(random.randint(0, 10000))
        A.append(line)
    return A

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

cProfile.run("run()", "matrix_mult.stats")
