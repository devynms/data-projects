cmake_minimum_required(VERSION 3.6)
project(demo)

set(CMAKE_CXX_STANDARD 14)

set(SOURCE_FILES
        main.cpp)

include_directories(solver)

add_executable(demo ${SOURCE_FILES})
target_link_libraries(demo solver)