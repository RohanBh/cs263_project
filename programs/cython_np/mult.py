import numpy as np


def main():
    n = 10000
    A = np.random.rand(n, n)
    B = np.random.rand(n, n)
    C = np.matmul(A, B)
    return


def time_main():
    import timeit
    print(timeit.timeit(main, number=1))
    return


if __name__ == "__main__":
    time_main()
