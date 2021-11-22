from setuptools import setup
from Cython.Build import cythonize
from distutils.extension import Extension

from Cython.Compiler.Options import get_directive_defaults
directive_defaults = get_directive_defaults()
#directive_defaults['linetrace'] = True
#directive_defaults['binding'] = True

setup(
    name='cannyEdge',
    #ext_modules=cythonize(Extension('canny_edge_cython', ['canny_edge_cython.pyx'], define_macros=[('CYTHON_TRACE', '1')])),
    ext_modules=cythonize(Extension('canny_edge_cython', ['canny_edge_cython.pyx'])),
    zip_safe=False,
)
