import construct

primary_header_primary_header = construct.Struct(
    "type" / construct.BytesInteger(1), "version" / construct.BytesInteger(1)
)

frame_v1_secondary_header = construct.Struct(
    "duration" / construct.BytesInteger(2), "data_length" / construct.BytesInteger(2)
)

frame_v1_tlc = construct.BitStruct(
    "state" / construct.Array(16, construct.BitsInteger(12))
)

frame_v1_frame_v1 = construct.Struct(
    "secondary_header" / frame_v1_secondary_header,
    "tlc_states"
    / construct.Array(construct.this.secondary_header.data_length // 24, frame_v1_tlc),
)

frame_frame = construct.Struct(
    "primary_header" / primary_header_primary_header,
    "frame"
    / construct.Switch(construct.this.primary_header.version, {1: frame_v1_frame_v1}),
)

animation_v1_secondary_header = construct.Struct(
    "name" / construct.PaddedString(32, "utf8"),
    "time" / construct.BytesInteger(8),
    "tlc_count" / construct.BytesInteger(1),
    "frame_count" / construct.BytesInteger(4),
    "data_length" / construct.BytesInteger(4),
)

animation_v1_animation_v1 = construct.Struct(
    "secondary_header" / animation_v1_secondary_header,
    "frames"
    / construct.Array(construct.this.secondary_header.frame_count, frame_frame),
)

animation_animation = construct.Struct(
    "primary_header" / primary_header_primary_header,
    "animation"
    / construct.Switch(
        construct.this.primary_header.version, {1: animation_v1_animation_v1}
    ),
    "sha256" / construct.Bytes(32),
)

library_v1_secondary_header = construct.Struct(
    "name" / construct.PaddedString(32, "utf8"),
    "time" / construct.BytesInteger(8),
    "animation_count" / construct.BytesInteger(4),
    "data_length" / construct.BytesInteger(8),
)

library_v1_library_v1 = construct.Struct(
    "secondary_header" / library_v1_secondary_header,
    "animations"
    / construct.Array(
        construct.this.secondary_header.animation_count, animation_animation
    ),
)

library_library = construct.Struct(
    "primary_header" / primary_header_primary_header,
    "library"
    / construct.Switch(
        construct.this.primary_header.version, {1: library_v1_library_v1}
    ),
    "sha256" / construct.Bytes(32),
)

cube_file_cube_file = construct.Struct(
    "primary_header" / primary_header_primary_header,
    "file"
    / construct.Switch(construct.this.primary_header.version, {1: library_library}),
)
