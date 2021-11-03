# Profiling Sieve of Eratosthenes
We call sieve to find prime numbers up to 20M.

## Python
Running `timeit`: 4.069404850248247

Running `line_profiler`
```
Timer unit: 1e-06 s

Total time: 23.2114 s
File: /mnt/hdd/Projects/cs263_project/programs/sieve/sieve_of_eratosthenes.py
Function: main_wrapper at line 29

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    29                                           def main_wrapper():
    30         1   23211368.0 23211368.0    100.0      main()
    31         1          1.0      1.0      0.0      return
```

## Cython
Running `timeit`: 3.199113440234214

Running `line_profiler`
```
Timer unit: 1e-06 s

Total time: 3.18674 s
File: /mnt/hdd/Projects/cs263_project/programs/sieve/time_sieve.py
Function: main_wrapper at line 12

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    12                                           def main_wrapper():
    13         1    3186735.0 3186735.0    100.0      main()
    14         1          1.0      1.0      0.0      return
```

## Cython Optimized (with types)
Running `timeit`: 1.3275476680137217

Running `line_profiler`
```
Timer unit: 1e-06 s

Total time: 1.30329 s
File: /mnt/hdd/Projects/cs263_project/programs/sieve/time_optim_sieve.py
Function: main_wrapper at line 12

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    12                                           def main_wrapper():
    13         1    1303290.0 1303290.0    100.0      main()
    14         1          1.0      1.0      0.0      return
```

# Conclusion
Somehow, running `line_profiler` improves the cython performance but makes the python performance much worse.
