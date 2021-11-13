# cython: profile=True
import pyximport
pyximport.install()

import io_profiling_cython_optim

PROFILER = "cProfile"

def wrapper():
    n = 2000000
    io_profiling_cython_optim.write_random_bytes(n)
    io_profiling_cython_optim.read_bytes(n)

if PROFILER == "cProfile":
    import cProfile
    cProfile.run("io_profiling_cython_optim.run()", "io_profiling_cython_optim_c.stats")
elif PROFILER == "line_profiler":
    # correct usage according to https://stackoverflow.com/a/43377717
    import line_profiler
    prof = line_profiler.LineProfiler()
    prof_wrapper = prof(wrapper)
    prof_wrapper()
    prof.print_stats()
elif PROFILER == "profile":
    import profile
    profile.run("io_profiling_cython_optimn.run()", "io_profiling_cython_optim_p.stats")
else:
    import sys
    print("unknown profiler")
    sys.exit(1)
