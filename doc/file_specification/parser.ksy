meta:
  id: parser
  imports:
    - objects/primary_header
    - objects/frame
    - objects/animation
    - objects/library
    - objects/cube_file
  endian: be

doc: |
  LED Cube Master Parser
  This parser looks at the primary header to determine how to parse the data
  provided. This parser is the recommended method to process data related to the
  LED Cube specification.

seq:
  - id: primary_header
    type: primary_header

instances:
  object:
    pos: 0
    type:
      switch-on: primary_header.type
      cases:
        'primary_header::type::frame': frame
        'primary_header::type::animation': animation
        'primary_header::type::library': library
        'primary_header::type::file': cube_file
    doc: This is where the data is actually parsed
