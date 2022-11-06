meta:
  id: library
  imports:
    - primary_header
    - library/library_v1
  endian: be

doc: LED Cube library

seq:
  - id: primary_header
    type: primary_header
  - id: library
    type:
      switch-on: primary_header.version
      cases:
        1: library_v1
    doc: The structure is determined by the version
