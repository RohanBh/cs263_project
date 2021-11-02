# cython: profile=True
import pyximport
pyximport.install()

import matrix_invert_cython_optim

PROFILER = "line_profiler"

def wrapper():
    n = 9
    A = matrix_invert_cython_optim.create_matrix(n)
    A_inv = matrix_invert_cython_optim.getMatrixInverse(A)
    res = matrix_invert_cython_optim.mult(A, A_inv, n)
    res_int = matrix_invert_cython_optim.mat_to_int(res)
    print(matrix_invert_cython_optim.check_ident(res_int))


if PROFILER == "cProfile":
    import cProfile
    cProfile.run("matrix_invert_cython_optim.run()", "matrix_invert_cython_optim_c.stats")
elif PROFILER == "line_profiler":
    # correct usage according to https://stackoverflow.com/a/43377717
    import line_profiler
    prof = line_profiler.LineProfiler()
    prof_wrapper = prof(wrapper)
    prof_wrapper()
    prof.print_stats()
elif PROFILER == "profile":
    import profile
    profile.run("matrix_invert_cython_optim.run()", "matrix_invert_cython_optim_p.stats")
else:
    import sys
    print("unknown profiler")
    sys.exit(1)
