#!/bin/bash

pushd ./led_cube_data/parser/ || exit 1
kaitai-struct-compiler -t python --python-package led_cube_data.parser ../../doc/file_specification/parser.ksy
popd || exit 2

# Patch parser.py
./tools/parser_patch.sh
