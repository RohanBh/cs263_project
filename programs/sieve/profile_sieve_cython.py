def time_main():
    import pyximport
    pyximport.install()
    from sieve_of_eratosthenes_cython import main
    import timeit
    import numpy as np

    time_arr = timeit.repeat(main, repeat=5, number=1)
    print('Times:', time_arr)
    print('Median:', np.median(time_arr))
    return

def main_wrapper():
    main()
    return

def profile_main():
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

def profile_all():
    from sieve_of_eratosthenes_cython import main, sieve
    import line_profiler

    prof = line_profiler.LineProfiler()
    prof.add_function(sieve)
    prof_wrapper = prof(main)
    prof_wrapper()
    prof.print_stats()
    return


if __name__ == "__main__":
    # time_main()
    # profile_main()
    # profile_sieve()
    profile_all()
