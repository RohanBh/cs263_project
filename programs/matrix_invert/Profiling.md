## Performance Measurements

* python: `3.347s, 3.363s, 3.415s, 3.409s, 3.393s`
* cython, no modifications, only compiled: `2.010s, 2.036s, 2.019s, 2.035s, 2.010s`
* cython, add basic types (state of `matrix_invert_cython.pyx`): `1.591s, 1.645s, 1.619s, 1.644s, 1.621s`
* add `cpdef` and some more remaining `int` types (state of `matrix_invert_cython_optim.pyx`): `1.581s, 1.595s, 1.588s, 1.600s, 1.607s`