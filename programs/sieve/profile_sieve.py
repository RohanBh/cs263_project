def main_wrapper():
    main()
    return


def time_main():
    from sieve_of_eratosthenes import main
    import timeit
    import numpy as np

    time_arr = timeit.repeat(main, repeat=5, number=1)
    print('Times:', time_arr)
    print('Median:', np.median(time_arr))
    return


def profile_main():
    from sieve_of_eratosthenes import main
    import line_profiler

    prof = line_profiler.LineProfiler()
    prof_main = prof(main_wrapper)
    prof_main()
    prof.print_stats()
    return


def profile_sieve():
    from sieve_of_eratosthenes import sieve
    import line_profiler

    prof = line_profiler.LineProfiler()
    prof_sieve = prof(sieve)
    prof_sieve(20000000)
    prof.print_stats()
    return


if __name__ == "__main__":
    time_main()
    # profile_main()
    # profile_sieve()