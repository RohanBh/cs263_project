from distutils.core import setup, Extension
from Cython.Build import cythonize

from Cython.Compiler.Options import get_directive_defaults
directive_defaults = get_directive_defaults()

directive_defaults['linetrace'] = True
directive_defaults['binding'] = True

extensions = [
    Extension("train_cython_typed", ["train_cython_typed.pyx"], define_macros=[('CYTHON_TRACE', '1')], include_dirs=[np.get_include()])
]

setup(
    name='train_cython_typed',
    ext_modules=cythonize(extensions),
)
