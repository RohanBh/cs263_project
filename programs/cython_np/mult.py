import numpy as np


def main():
    n = 10000
    A = np.random.rand(n, n)
    B = np.random.rand(n, n)
    C = np.matmul(A, B)
    return


def time_main():
    import timeit
    time_arr = timeit.repeat(main, repeat=5, number=1)
    print('Times:', time_arr)
    print('Median:', np.median(time_arr))
    return


if __name__ == "__main__":
    time_main()
