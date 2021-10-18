## CS263 Project


* `programs/matrix_mult.py`: simple matrix-matrix multiplication to familiarize with profilers
* `programs/heap_sort,py`: simple heap-sort implementation to familiarize with profilers
* `programs/*cython*.pyx`: first attempt at profiling setup for cython
* `tools/print_stats.py`: utility program to print stat dumps created by `cProfile`/`profile`

### Profilers

* `cProfile` - deterministic, see [cProfile docs](https://docs.python.org/3/library/profile.html)
* `line_profiler` - deterministic, see [line_profiler repo](https://github.com/pyutils/line_profiler)
* `profile` - deterministic, see [profile docs](https://docs.python.org/3/library/profile.html)

### Setup

* Install line_profiler: `pip install line_profiler`
* Install cython: `pip install cython`