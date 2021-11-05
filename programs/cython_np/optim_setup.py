from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy as np

extensions = [
    Extension("mult_optim_cython", ["mult_optim_cython.pyx"], include_dirs=[np.get_include()])
]

setup(
    name='sieve_cython',
    ext_modules=cythonize(extensions),
)
