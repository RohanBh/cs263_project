from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy as np

extensions = [
    Extension("train_cython_typed", ["train_cython_typed.pyx"], include_dirs=[np.get_include()])
]

setup(
    name='train_cython_typed',
    ext_modules=cythonize(extensions),
)
