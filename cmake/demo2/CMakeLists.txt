cmake_minimum_required (VERSION 3.11)

project (demo2)

# add_executable(demo2 main.cpp lib.cpp)

aux_source_directory(. src_dir)	# equals set src_dir=.

add_executable(Demo2B ${src_dir})
