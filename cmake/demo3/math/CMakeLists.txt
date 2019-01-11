# the CMakeLists.txt in the math sub-dir

aux_source_directory (. lib_dir)

# compile to library (*.lib)
add_library (lib ${lib_dir})
