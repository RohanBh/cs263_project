from distutils.core import setup, Extension
from Cython.Build import cythonize

# https://stackoverflow.com/a/28301932/7263373
# So that linetrace works with Cython
from Cython.Compiler.Options import get_directive_defaults
directive_defaults = get_directive_defaults()

directive_defaults['linetrace'] = True
directive_defaults['binding'] = True

extensions = [
    Extension("sieve_of_eratosthenes_cython", ["sieve_of_eratosthenes_cython.pyx"], define_macros=[('CYTHON_TRACE', '1')])
]

setup(
    name='sieve_cython',
    ext_modules=cythonize(extensions),
)
