# cython: profile=True
#import pyximport
#pyximport.install()

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
    """
    prof_wrapper = prof(wrapper)
    prof_wrapper()
    """
    """
    n = 200000
    arr = heap_sort_cython_optim.create_array(n)
    prof_wrapper = prof(heap_sort_cython_optim.heapSort)
    prof_wrapper(arr)
    """
    n = 200000
    arr = heap_sort_cython_optim.create_array(n)
    for i in range(n, -1, -1):
        heap_sort_cython_optim.heapify(arr, n, i)
    arr[n-1], arr[0] = arr[0], arr[n-1]
    prof_wrapper = prof(heap_sort_cython_optim.heapify)
    prof_wrapper(arr, n-1, 0)
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
