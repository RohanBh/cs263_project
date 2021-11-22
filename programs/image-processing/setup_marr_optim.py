from setuptools import setup
from Cython.Build import cythonize
from distutils.extension import Extension

from Cython.Compiler.Options import get_directive_defaults
directive_defaults = get_directive_defaults()

setup(
    name='Marr Hildreth',
    ext_modules=cythonize(Extension('marr_cython_optim', ['marr_cython_optim.pyx'])),
    zip_safe=False,
)
