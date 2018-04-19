from setuptools import setup, Extension

#
# Extension
#

SOLVER_ROOT = 'c_solver/solver'
SOLVER_SRCS = ['solver.cpp', 'solvermodule.cpp']

SOLVER_FILES = list(map(lambda src: f'{SOLVER_ROOT}/{src}', SOLVER_SRCS))

solver_extension = Extension(
        'solver',
        SOLVER_FILES,
        include_dirs=[SOLVER_ROOT],
        extra_compile_args=['-std=c++14'],
        extra_link_args=['-larmadillo'])

#
# Setup
#

setup(name='sudoku-learning',
      version='1.0',
      author='Devyn Spillane',
      python_requires='>=3',
      packages=[
          'training',
          'solving'
      ],
      install_requires=[
          'numpy',
          'scipy',
          'scikit-learn',
          'matplotlib'
      ],
      ext_modules=[
          solver_extension
      ],
      scripts=[
          'scripts/logitdata',
          'scripts/trainlogit'
      ],
      setup_requires=[
          'pytest-runner'
      ],
      tests_require=[
          'pytest'
      ])
