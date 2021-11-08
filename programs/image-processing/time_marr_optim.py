import pyximport
pyximport.install()

import marr_cython_optim
import timeit

print(timeit.timeit(marr_cython_optim.main, number=1))
