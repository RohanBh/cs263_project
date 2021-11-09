## Performance Measurements

* python: `1.487s, 1.490s, 1.532s, 1.568s, 1.536s`
* cython, no types added: `1.065s, 0.921s, 0.917s, 0.929s, 0.930s`
* cython, add types only to heapify (current state of `heap_sort_cython.pyx`): `0.518s, 0.525s, 0.525s, 0.520s, 0.535s`
* add as many types as possible, including return types (see `heap_sort_cython_optim.pyx`): `0.192s, 0.195s, 0.184s, 0.191s, 0.187s`
