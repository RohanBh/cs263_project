## Performance Measurements

### Canny-Edge

* python: `19.311s, 19.443s, 20.272s, 19.591s, 20.822s`
* cython, no type info added: `19.408s, 19.396s, 19.456s, 20.039s, 19.940s`
* cython, int types and one float added, current state of `canny_edge_cython.pyx`: `19.877s, 19.798s, 20.881s, 19.688s, 19.499s`

### Marr Hildreth Edge

* Python: `8.694, 8.737, 8.832s, 8.816s, 8.909s`
* Cython, no type info added: `8.636s, 8.624s, 8.432s, 8.477s, 8.513s`
* Cython, ints and one float added (current state of `marr_cython_optim.pyx`): `7.490s, 7.655s, 7.740s, 7.693s, 7.555s`