import pyximport
pyximport.install()

import marr_cython
import timeit

print(timeit.repeat(marr_cython.main, repeat=5, number=1))
