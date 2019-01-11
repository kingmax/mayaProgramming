cmake_minimum_required (VERSION 3.11)

project (demo3)

aux_source_directory (. src_dir)

add_subdirectory(math)

add_executable (demo3 main.cpp)

# link the lib
target_link_libraries (demo3 lib)


