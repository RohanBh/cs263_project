def time_main():
    import pyximport
    pyximport.install()
    from mult_cython import main
    import timeit
    print(timeit.timeit(main, number=1))
    return


if __name__ == "__main__":
    time_main()
