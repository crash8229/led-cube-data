meta:
  id: primary_header
  endian: be

doc: Used in all objects to specify the type and version

seq:
  - id: type
    type: u1
    enum: type
  - id: version
    type: u1

enums:
  type:
    0: frame
    1: animation
    2: library
    3: file
