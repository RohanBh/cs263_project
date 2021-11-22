from setuptools import setup
from Cython.Build import cythonize
from distutils.extension import Extension

from Cython.Compiler.Options import get_directive_defaults
directive_defaults = get_directive_defaults()

setup(
    name='cannyEdge',
    ext_modules=cythonize(Extension('canny_edge', ['canny_edge.pyx'])),
    zip_safe=False,
)
