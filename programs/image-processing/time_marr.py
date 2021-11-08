import pyximport
pyximport.install()

import marr_cython
import timeit

print(timeit.timeit(marr_cython.main, number=1))
