#import pyximport
#pyximport.install()

import marr_cython_optim
import timeit

print(timeit.repeat(marr_cython_optim.main, repeat=5, number=1))
