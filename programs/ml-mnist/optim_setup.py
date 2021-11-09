from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy as np

extensions = [
    Extension("train_and_evaluate_optim_cython", ["train_and_evaluate_optim_cython.pyx"], include_dirs=[np.get_include()])
]

setup(
    name='train_mnist',
    ext_modules=cythonize(extensions),
)
