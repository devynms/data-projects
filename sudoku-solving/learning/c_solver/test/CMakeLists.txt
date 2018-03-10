set(CMAKE_CXX_STANDARD 14)

include_directories(${gtest_SOURCE_DIR} ${gtest_SOURCE_DIR}/include)
include_directories(${solver_SOURCE_DIR})

add_executable(solver_test
        test_solver.cpp)

target_link_libraries(solver_test gtest gtest_main)
target_link_libraries(solver_test solver)
