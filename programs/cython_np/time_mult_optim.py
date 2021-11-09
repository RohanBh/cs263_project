def time_main():
    from mult_optim_cython import main
    import timeit
    import numpy as np
    time_arr = timeit.repeat(main, repeat=5, number=1)
    print('Times:', time_arr)
    print('Median:', np.median(time_arr))
    return


if __name__ == "__main__":
    time_main()
