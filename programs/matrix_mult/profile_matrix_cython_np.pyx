# cython: profile=True
import pyximport
pyximport.install()

import matrix_mult_cython_np

PROFILER = "line_profiler"

def wrapper():
    n = 900
    A = matrix_mult_cython_np.create_matrix(n)
    #matrix_mult_cython_np.print_matrix(A)
    B = matrix_mult_cython_np.create_matrix(n)
    #matrix_mult_cython_np.print_matrix(B)
    result = matrix_mult_cython_np.mult(A, B, n)
    #matrix_mult_cython_np.print_matrix(result)



if PROFILER == "cProfile":
    import cProfile
    cProfile.run("matrix_mult_cython.run()", "matrix_mult_cython_c.stats")
elif PROFILER == "line_profiler":
    # correct usage according to https://stackoverflow.com/a/43377717
    import line_profiler
    prof = line_profiler.LineProfiler()
    prof_wrapper = prof(wrapper)
    prof_wrapper()
    prof.print_stats()
elif PROFILER == "profile":
    import profile
    profile.run("matrix_mult_cython.run()", "matrix_mult_cython_p.stats")
else:
    import sys
    print("unknown profiler")
    sys.exit(1)
