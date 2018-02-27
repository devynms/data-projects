cmake_minimum_required(VERSION 3.6)
project(solver)

set(CMAKE_CXX_STANDARD 14)

set(SOURCE_FILES
        search.cpp
        search.h
        state.cpp
        state.h)

add_library(solver SHARED STATIC ${SOURCE_FILES})