## Why this benchmark?
Interpretation is problematic for computation-heavy workloads. HeapSort is a CPU-bound algorithm
but has a different memory access pattern and different operations than typical matrix operations.

## Performance Measurements overall

* python: `1.487s, 1.490s, 1.532s, 1.568s, 1.536s`
* cython, no types added: `1.065s, 0.921s, 0.917s, 0.929s, 0.930s`
* cython, add types only to heapify (current state of `heap_sort_cython.pyx`): `0.518s, 0.525s, 0.525s, 0.520s, 0.535s`
* add as many types as possible, including return types (see `heap_sort_cython_optim.pyx`): `0.192s, 0.195s, 0.184s, 0.191s, 0.187s`
-> there is a speedup, why?

## Performance detailed

* Python, main
```
Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    51                                           def main():
    52         1          4.0      4.0      0.0      n = 200000
    53         1     628993.0 628993.0     10.5      arr = create_array(n)
    54         1    5351855.0 5351855.0     89.5      heapSort(arr)
    55         1          1.0      1.0      0.0      if PRINT:
    56                                                   print_array(arr)
```

* Cython, main

```
Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     9                                           def wrapper():
    10         1          1.0      1.0      0.0      n = 200000
    11         1     547426.0 547426.0     42.8      arr = heap_sort_cython.create_array(n)
    12         1     730992.0 730992.0     57.2      heap_sort_cython.heapSort(arr)
```

* Cython - typed, main (TODO: enable better profiling of this)

```
Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     9                                           def wrapper():
    10         1     616744.0 616744.0    100.0      heap_sort_cython_optim.main()
```
