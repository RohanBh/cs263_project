#!/usr/bin/env python3
import pyximport
pyximport.install()

import canny_edge_cython
import timeit

print(timeit.repeat(canny_edge_cython.main, repeat=5, number=1))
