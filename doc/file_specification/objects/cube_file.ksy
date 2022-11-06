meta:
  id: cube_file
  imports:
    - primary_header
    - library
  endian: be

doc: LED Cube file

seq:
  - id: primary_header
    type: primary_header
  - id: file
    type:
      switch-on: primary_header.version
      cases:
        1: library
    doc: The structure is determined by the version
