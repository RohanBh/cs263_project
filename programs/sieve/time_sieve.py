def time_main():
    from sieve_of_eratosthenes_cython import main
    import timeit
    print(timeit.timeit(main, number=1))
    return

def main_wrapper():
    main()
    return

def profile_main():
    import pyximport
    pyximport.install()

    from sieve_of_eratosthenes_cython import main

    import line_profiler
    prof = line_profiler.LineProfiler()
    prof_main = prof(main_wrapper)
    prof_main()
    prof.print_stats()
    return

def profile_sieve():
    from sieve_of_eratosthenes_cython import sieve
    import line_profiler
    prof = line_profiler.LineProfiler()
    prof_sieve = prof(sieve)
    prof_sieve(20000000)
    prof.print_stats()
    return


if __name__ == "__main__":
    # time_main()
    # profile_main()
    profile_sieve()
