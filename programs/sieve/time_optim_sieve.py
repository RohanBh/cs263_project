import pyximport
pyximport.install()

from sieve_of_eratosthenes_optim_cython import main


def time_main():
    import timeit
    print(timeit.timeit(main, number=1))
    return

def main_wrapper():
    main()
    return

def profile_main():
    import line_profiler
    prof = line_profiler.LineProfiler()
    prof_main = prof(main_wrapper)
    prof_main()
    prof.print_stats()
    return


if __name__ == "__main__":
    # time_main()
    profile_main()

