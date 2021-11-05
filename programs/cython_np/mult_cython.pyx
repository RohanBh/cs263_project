#cython: language_level=3
import numpy as np


def main():
    n = 10000
    A = np.random.rand(n, n)
    B = np.random.rand(n, n)
    C = np.matmul(A, B)
    return
