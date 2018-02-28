cmake_minimum_required(VERSION 3.6)
project(solve)

set(CMAKE_CXX_STANDARD 14)

set(SOURCE_FILES
        parse.cpp
        main.cpp)

include_directories(${solver_SOURCE_DIR})

add_executable(solve ${SOURCE_FILES})
target_link_libraries(solve solver)