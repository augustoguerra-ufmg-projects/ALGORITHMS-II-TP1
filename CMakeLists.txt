set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
cmake_minimum_required(VERSION 3.15...3.27)
project(tp1)

add_executable(kdtree_test src/kdtree_test.cpp)
target_include_directories(kdtree_test PRIVATE include)
