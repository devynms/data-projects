from distutils.core import setup, Extension

SOLVER_ROOT = 'c_solver/solver'
SOLVER_SRCS = ['solver.cpp', 'solvermodule.cpp']

SOLVER_FILES = list(map(lambda src: f'{SOLVER_ROOT}/{src}', SOLVER_SRCS))

solver_extension = Extension(
        'solver',
        SOLVER_FILES,
        include_dirs=[SOLVER_ROOT],
        extra_compile_args=['-std=c++14'],
        extra_link_args=['-larmadillo'])

setup(name='learning',
      version='1.0',
      ext_modules=[solver_extension])
