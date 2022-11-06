meta:
  id: animation
  imports:
    - primary_header
    - animation/animation_v1
  endian: be

doc: LED Cube animation

seq:
  - id: primary_header
    type: primary_header
  - id: animation
    type:
      switch-on: primary_header.version
      cases:
        1: animation_v1
    doc: The structure is determined by the version
  - id: crc
    type: u4
    doc: CRC of the contents in animation
