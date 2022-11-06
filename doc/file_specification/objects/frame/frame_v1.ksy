meta:
  id: frame_v1
  endian: be

doc: Version 1 of the frame specification

seq:
  - id: secondary_header
    type: secondary_header
  - id: tlc_states
    type: tlc
    repeat: expr
    repeat-expr: secondary_header.data_length / 24
    
types:
  secondary_header:
    doc: Houses the frame duration and data length
    seq:
      - id: duration
        type: u2
        doc: How long to display the frame in ms
      - id: data_length
        type: u2
        doc: Number of bytes after the header
  tlc:
    doc: LED states for a single TLC 5940
    seq:
      - id: state
        type: b12
        repeat: expr
        repeat-expr: 16
