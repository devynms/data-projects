cmake_minimum_required(VERSION 3.6)

set(CMAKE_CXX_STANDARD 14)

include_directories(${gtest_SOURCE_DIR}/include ${gtest_SOURCE_DIR})
include_directories(${solver_SOURCE_DIR})

add_executable(solver_test
        search_check.cpp
        state_check.cpp)

target_link_libraries(solver_test gtest gtest_main)
target_link_libraries(solver_test solver)
