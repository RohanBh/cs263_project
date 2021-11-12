# cython: profile=True
import pyximport
pyximport.install()

import heap_sort_cython_optim

PROFILER = "line_profiler"

def wrapper():
    n = 200000
    arr = heap_sort_cython_optim.create_array(n)
    heap_sort_cython_optim.heapSort(arr)
    #heap_sort_cython_optim.main()


if PROFILER == "cProfile":
    import cProfile
    cProfile.run("heap_sort_cython.main()", "heap_sort_cython_c.stats")
elif PROFILER == "line_profiler":
    # correct usage according to https://stackoverflow.com/a/43377717
    import line_profiler
    prof = line_profiler.LineProfiler()
    prof_wrapper = prof(wrapper)
    prof_wrapper()
    prof.print_stats()
elif PROFILER == "profile":
    import profile
    profile.run("heap_sort_cython.main()", "heap_sort_cython_p.stats")
elif PROFILER == "timeit":
    import timeit
    print(timeit.repeat(heap_sort_cython_optim.main, repeat=5, number=1))
else:
    import sys
    print("unknown profiler")
    sys.exit(1)
