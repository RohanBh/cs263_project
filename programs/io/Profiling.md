## Why this benchmark?
We want to find out whether compilation can also improve access speed to the harddisc.

## Performance measurements

**Python**

```
Total time: 0.135425 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    18                                           def run():
    19         1          4.0      4.0      0.0      n = 200000
    20         1     135335.0 135335.0     99.9      write_random_bytes(n)
    21         1         86.0     86.0      0.1      read_bytes(n)
```

**Cython, no types**

```
Total time: 0.013508 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     9                                           def wrapper():
    10         1          1.0      1.0      0.0      n = 20000
    11         1      13449.0  13449.0     99.6      io_profiling_cython.write_random_bytes(n)
    12         1         58.0     58.0      0.4      io_profiling_cython.read_bytes(n)
```

**Cython, typed**

```
Total time: 0.013474 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     9                                           def wrapper():
    10         1          2.0      2.0      0.0      n = 20000
    11         1      13426.0  13426.0     99.6      io_profiling_cython_optim.write_random_bytes(n)
    12         1         46.0     46.0      0.3      io_profiling_cython_optim.read_bytes(n)
```
 * measurements are very close
 * multiple executions show, that the distance between the two measurements above lie within the measurement uncertainty

Try larger number of bytes, hoping that potential differences will become bigger than the uncertainty.

**Python**

```
Total time: 1.35616 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    18                                           def run():
    19         1          2.0      2.0      0.0      n = 2000000
    20         1    1354928.0 1354928.0     99.9      write_random_bytes(n)
    21         1       1228.0   1228.0      0.1      read_bytes(n)
```

**Cython, no types**

```
Total time: 1.34728 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     9                                           def wrapper():
    10         1          1.0      1.0      0.0      n = 2000000
    11         1    1346103.0 1346103.0     99.9      io_profiling_cython.write_random_bytes(n)
    12         1       1176.0   1176.0      0.1      io_profiling_cython.read_bytes(n)
```

**Cython, typed**

```
Total time: 1.34791 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     9                                           def wrapper():
    10         1          4.0      4.0      0.0      n = 2000000
    11         1    1346320.0 1346320.0     99.9      io_profiling_cython_optim.write_random_bytes(n)
    12         1       1591.0   1591.0      0.1      io_profiling_cython_optim.read_bytes(n)
```

 * same problem as with first measurement
 * apparently no difference -> why?

**Investigation with cProfile**
```
         4000021 function calls in 1.169 seconds

   Random listing order was used

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    1.169    1.169 {built-in method builtins.exec}
        2    0.000    0.000    0.000    0.000 {built-in method builtins.len}
  2000000    0.117    0.000    0.117    0.000 {method 'random' of '_random.Random' objects}
        2    0.000    0.000    0.000    0.000 {built-in method _locale.nl_langinfo}
  2000000    0.623    0.000    0.623    0.000 {built-in method _bisect.bisect_right}
        1    0.001    0.001    0.001    0.001 {built-in method _codecs.utf_8_decode}
        1    0.000    0.000    1.169    1.169 <string>:1(<module>)
        1    0.000    0.000    1.169    1.169 io_profiling_cython_optim.pyx:20(run)
        1    0.001    0.001    0.002    0.002 io_profiling_cython_optim.pyx:15(read_bytes)
        1    0.024    0.024    1.167    1.167 io_profiling_cython_optim.pyx:9(write_random_bytes)
        1    0.000    0.000    1.169    1.169 {io_profiling_cython_optim.run}
        1    0.403    0.403    1.143    1.143 /usr/lib/python3.8/random.py:408(<listcomp>)
        1    0.000    0.000    1.143    1.143 /usr/lib/python3.8/random.py:386(choices)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        2    0.000    0.000    0.000    0.000 /usr/lib/python3.8/_bootlocale.py:33(getpreferredencoding)
        1    0.000    0.000    0.000    0.000 /usr/lib/python3.8/codecs.py:260(__init__)
        1    0.000    0.000    0.000    0.000 /usr/lib/python3.8/codecs.py:309(__init__)
        1    0.000    0.000    0.001    0.001 /usr/lib/python3.8/codecs.py:319(decode)
        1    0.000    0.000    0.000    0.000 /usr/lib/python3.8/codecs.py:331(getstate)
        1    0.000    0.000    0.000    0.000 /usr/lib/python3.8/codecs.py:186(__init__)
```

apparently, the random generation takes the major part of the execution, not writing the bytes to disc or reading from there.
Random generation is in library, where we have no annotations -> it is not surprising, that the annotations do not improve performance.
Cython does not improve the performance, since, the random method, which is the biggest slowdown, is already implemented in C (see comment in /usr/lib/python3.8/random.py:35-36)