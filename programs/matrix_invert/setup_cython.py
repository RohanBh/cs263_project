from setuptools import setup
from Cython.Build import cythonize
from distutils.extension import Extension

from Cython.Compiler.Options import get_directive_defaults
directive_defaults = get_directive_defaults()
directive_defaults['linetrace'] = True
directive_defaults['binding'] = True

setup(
    name='MatrixInversion',
    ext_modules=cythonize(Extension('matrix_invert_cython', ['matrix_invert_cython.pyx'], define_macros=[('CYTHON_TRACE', '1')])),
    zip_safe=False,
)

extensions = [
    Extension('test', ['test.pyx'], define_macros=[('CYTHON_TRACE', '1')])
]
