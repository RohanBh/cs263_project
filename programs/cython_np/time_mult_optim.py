def time_main():
    from mult_optim_cython import main
    import timeit
    print(timeit.timeit(main, number=1))
    return


if __name__ == "__main__":
    time_main()
