cmake_minimum_required(VERSION 3.6)
project(solver)

set(CMAKE_CXX_STANDARD 14)

if(APPLE)
    include_directories(/usr/local/Cellar/python3/3.6.1/Frameworks/Python.framework/Versions/3.6/include/python3.6m)
else()
    find_package(PythonLibs 3.6 REQUIRED)
    include_directories(${PYTHON_INCLUDE_DIRS})
endif()

set(SOURCES
        solver.cpp
        solvermodule.cpp)

add_library(solver SHARED STATIC ${SOURCES})
