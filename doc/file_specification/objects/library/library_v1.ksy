meta:
  id: library_v1
  imports:
    - ../animation
  endian: be

doc: Version 1 of the library specification

seq:
  - id: secondary_header
    type: secondary_header
  - id: crc
    type: u4
    doc: CRC of the secondary header
  - id: animations
    type: animation
    repeat: expr
    repeat-expr: secondary_header.animation_count

types:
  secondary_header:
    doc: Houses the library metadata
    seq:
      - id: name
        type: str
        size: 32
        encoding: UTF-8
        doc: Name of the animation
      - id: time
        type: u8
        doc: UNIX timestamp of file creation
      - id: animation_count
        type: u4
        doc: Number of animations in the library
      - id: data_length
        type: u8
        doc: Number of bytes after the header
