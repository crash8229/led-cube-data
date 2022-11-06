meta:
  id: animation_v1
  imports:
    - ../frame
  endian: be

doc: Version 1 of the animation specification

seq:
  - id: secondary_header
    type: secondary_header
  - id: frames
    type: frame
    repeat: expr
    repeat-expr: secondary_header.frame_count

types:
  secondary_header:
    doc: Houses the animation metadata
    seq:
      - id: name
        type: str
        size: 32
        encoding: UTF-8
        doc: Name of the animation
      - id: time
        type: u8
        doc: UNIX timestamp of file creation
      - id: tlc_count
        type: u1
        doc: Number of TLC 5940 chained together
      - id: frame_count
        type: u4
        doc: Number of frames in the animation
      - id: data_length
        type: u4
        doc: Number of bytes after the header
