## CS263 Project


* `programs/matrix_mult.py`: simple matrix-matrix multiplication to familiarize with profilers
* `programs/heap_sort,py`: simple heap-sort implementation to familiarize with profilers
* `programs/io_profiling.py`: program for measuring io performance
* `programs/matrix_invert.py`: simple matrix-inversion without numpy
* `programs/*cython*.pyx`: first attempts at profiling setup for cython
* `tools/print_stats.py`: utility program to print stat dumps created by `cProfile`/`profile`

### Profilers

* `cProfile` - deterministic, see [cProfile docs](https://docs.python.org/3/library/profile.html)
* `line_profiler` - deterministic, see [line_profiler repo](https://github.com/pyutils/line_profiler)
* `profile` - deterministic, see [profile docs](https://docs.python.org/3/library/profile.html)

### Setup

* Install line_profiler: `pip install line_profiler`
* Install cython: `pip install cython`

### General Notes

* compiling Python to C and from C to binary has no performance advantage over importing via
```
import pyximport
pyximport.install()
import your_fav_module
`
* compiling the profiler into the binary does not work, since necessary information for the profilers is lost during compilation