meta:
  id: frame
  imports:
    - primary_header
    - frame/frame_v1
  endian: be

doc: Single animation frame

seq:
  - id: primary_header
    type: primary_header
  - id: frame
    type:
      switch-on: primary_header.version
      cases:
        1: frame_v1
    doc: The structure is determined by the version
