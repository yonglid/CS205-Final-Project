from distutils.core import setup
from distutils.extension import Extension 

from Cython.Build import cythonize

ext_modules = [
	Extension(
		'full_write_par',
		['full_write_par.pyx'],
		extra_compile_args=['-fopenmp'],
		extra_link_args=['-fopenmp'],
		)
	]

setup(
  name = 'full_write_par',
  ext_modules=cythonize(ext_modules),
)

