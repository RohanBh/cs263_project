#!/usr/bin/env python3
import pyximport
pyximport.install()

import canny_edge
import timeit

print(timeit.repeat(canny_edge.main, repeat=5, number=1))
