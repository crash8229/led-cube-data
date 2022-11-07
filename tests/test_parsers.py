import led_cube_data
import pytest_check as check # type: ignore[import]


def test_frame_v1():
    p = led_cube_data.Parser.from_file("./doc/file_specification/objects/frame/frame_v1.bin")

    # Frame Primary Header in parser
    check.equal(p.primary_header.type.value, 0, "type was not 0")
    check.equal(p.primary_header.type.name, "frame", "type was not \"frame\"")
    check.equal(p.primary_header.version, 1, "version was not 1")

    # Frame Primary Header in object
    check.equal(p.object.primary_header.type.value, p.primary_header.type.value, "Difference in Type value for parser primary header and object primary header")
    check.equal(p.object.primary_header.type.name, p.primary_header.type.name, "Difference in Type symbol for parser primary header and object primary header")
    check.equal(p.object.primary_header.version, p.primary_header.version, "Difference in Version for parser primary header and object primary header")

    # Frame Secondary Header
    check.equal(p.object.frame.secondary_header.duration, 5, "duration was not 5")
    check.equal(p.object.frame.secondary_header.data_length, 48, "data_length was not 48")

    # Frame TLC States
    check.equal(p.object.frame.tlc_states[0].state, [0xAAA]*16, "tlc 0 states were not all 0xA")
    check.equal(p.object.frame.tlc_states[1].state, [0xBBB]*16, "tlc 1 states were not all 0xB")


def test_animation_v1():
    p = led_cube_data.Parser.from_file("./doc/file_specification/objects/animation/animation_v1.bin")

    # Animation Primary Header in parser
    check.equal(p.primary_header.type.value, 1, "type was not 1")
    check.equal(p.primary_header.type.name, "animation", "type was not \"animation\"")
    check.equal(p.primary_header.version, 1, "version was not 1")

    # Animation Primary Header in object
    check.equal(p.object.primary_header.type.value, p.primary_header.type.value, "Difference in Type value for parser primary header and object primary header")
    check.equal(p.object.primary_header.type.name, p.primary_header.type.name, "Difference in Type symbol for parser primary header and object primary header")
    check.equal(p.object.primary_header.version, p.primary_header.version, "Difference in Version for parser primary header and object primary header")

    # Animation Secondary Header
    check.equal(p.object.animation.secondary_header.name, "Test" + "\0"*28, "name was not \"Test\"")
    check.equal(p.object.animation.secondary_header.time, 0x3E8, "time was not 0x3E8")
    check.equal(p.object.animation.secondary_header.tlc_count, 2, "tlc_count was not 2")
    check.equal(p.object.animation.secondary_header.frame_count, 3, "frame_count was not 3")
    check.equal(p.object.animation.secondary_header.data_length, 0xA6, "data_length was not 0xA6")

    ################################################################################################

    # Frame 0 Primary Header in object
    check.equal(p.object.animation.frames[0].primary_header.type.value, 0, "frame 0 type was not 0")
    check.equal(p.object.animation.frames[0].primary_header.type.name, "frame", "frame 0 type was not \"frame\"")
    check.equal(p.object.animation.frames[0].primary_header.version, 1, "frame 0 version was not 1")

    # Frame 0 Secondary Header
    check.equal(p.object.animation.frames[0].frame.secondary_header.duration, 5, "frame 0 duration was not 5")
    check.equal(p.object.animation.frames[0].frame.secondary_header.data_length, 48, "frame 0 data_length was not 48")

    # Frame 0 TLC States
    check.equal(p.object.animation.frames[0].frame.tlc_states[0].state, [0xAAA]*16, "frame 0 tlc 0 states were not all 0xA")
    check.equal(p.object.animation.frames[0].frame.tlc_states[1].state, [0xBBB]*16, "frame 0 tlc 1 states were not all 0xB")

    ################################################################################################

    # Frame 1 Primary Header in object
    check.equal(p.object.animation.frames[1].primary_header.type.value, 0, "frame 1 type was not 0")
    check.equal(p.object.animation.frames[1].primary_header.type.name, "frame", "frame 1 type was not \"frame\"")
    check.equal(p.object.animation.frames[1].primary_header.version, 1, "frame 1 version was not 1")

    # Frame 1 Secondary Header
    check.equal(p.object.animation.frames[1].frame.secondary_header.duration, 5, "frame 1 duration was not 5")
    check.equal(p.object.animation.frames[1].frame.secondary_header.data_length, 48, "frame 1 data_length was not 48")

    # Frame 1 TLC States
    check.equal(p.object.animation.frames[1].frame.tlc_states[0].state, [0xCCC]*16, "frame 1 tlc 0 states were not all 0xC")
    check.equal(p.object.animation.frames[1].frame.tlc_states[1].state, [0xDDD]*16, "frame 1 tlc 1 states were not all 0xD")

    ################################################################################################

    # Frame 2 Primary Header in object
    check.equal(p.object.animation.frames[2].primary_header.type.value, 0, "frame 2 type was not 0")
    check.equal(p.object.animation.frames[2].primary_header.type.name, "frame", "frame 2 type was not \"frame\"")
    check.equal(p.object.animation.frames[2].primary_header.version, 1, "frame 2 version was not 1")

    # Frame 2 Secondary Header
    check.equal(p.object.animation.frames[2].frame.secondary_header.duration, 5, "frame 2 duration was not 5")
    check.equal(p.object.animation.frames[2].frame.secondary_header.data_length, 48, "frame 2 data_length was not 48")

    # Frame 2 TLC States
    check.equal(p.object.animation.frames[2].frame.tlc_states[0].state, [0xEEE]*16, "frame 2 tlc 0 states were not all 0xE")
    check.equal(p.object.animation.frames[2].frame.tlc_states[1].state, [0xFFF]*16, "frame 2 tlc 1 states were not all 0xF")

    ################################################################################################

    # SHA256
    check.equal(
        p.object.sha256,
        bytes.fromhex("04CA 25AA B4F3 284D EB20 2589 A68E 4202 99D9 7EF3 A94E 872B B3C1 0D5A 00FB 3650"),
        "sha256 was not: 04CA 25AA B4F3 284D EB20 2589 A68E 4202 99D9 7EF3 A94E 872B B3C1 0D5A 00FB 3650"
    )


def test_library_v1():
    p = led_cube_data.Parser.from_file("./doc/file_specification/objects/library/library_v1.bin")

    # Library Primary Header in parser
    check.equal(p.primary_header.type.value, 2, "type was not 2")
    check.equal(p.primary_header.type.name, "library", "type was not \"library\"")
    check.equal(p.primary_header.version, 1, "version was not 1")

    # Library Primary Header in object
    check.equal(p.object.primary_header.type.value, p.primary_header.type.value, "Difference in Type value for parser primary header and object primary header")
    check.equal(p.object.primary_header.type.name, p.primary_header.type.name, "Difference in Type symbol for parser primary header and object primary header")
    check.equal(p.object.primary_header.version, p.primary_header.version, "Difference in Version for parser primary header and object primary header")

    # Library Secondary Header
    check.equal(p.object.library.secondary_header.name, "Test Library" + "\0"*20, "name was not \"Test Library\"")
    check.equal(p.object.library.secondary_header.time, 0x3E8, "time was not 0x3E8")
    check.equal(p.object.library.secondary_header.animation_count, 2, "animation_count was not 2")
    check.equal(p.object.library.secondary_header.data_length, 0x1B6, "data_length was not 0x1B6")

    ################################################################################################

    # Animation 0 Primary Header in parser
    check.equal(p.object.library.animations[0].primary_header.type.value, 1, "animation 0 type was not 1")
    check.equal(p.object.library.animations[0].primary_header.type.name, "animation", "animation 0 type was not \"animation\"")
    check.equal(p.object.library.animations[0].primary_header.version, 1, "animation 0 version was not 1")

    # Animation 0 Secondary Header
    check.equal(p.object.library.animations[0].animation.secondary_header.name, "Test" + "\0"*28, "animation 0 name was not \"Test\"")
    check.equal(p.object.library.animations[0].animation.secondary_header.time, 0x3E8, "animation 0 time was not 0x3E8")
    check.equal(p.object.library.animations[0].animation.secondary_header.tlc_count, 2, "animation 0 tlc_count was not 2")
    check.equal(p.object.library.animations[0].animation.secondary_header.frame_count, 3, "animation 0 frame_count was not 3")
    check.equal(p.object.library.animations[0].animation.secondary_header.data_length, 0xA6, "animation 0 data_length was not 0xA6")

    ##############################################

    # Animation 0 Frame 0 Primary Header in object
    check.equal(p.object.library.animations[0].animation.frames[0].primary_header.type.value, 0, "animation 0 frame 0 type was not 0")
    check.equal(p.object.library.animations[0].animation.frames[0].primary_header.type.name, "frame", "animation 0 frame 0 type was not \"frame\"")
    check.equal(p.object.library.animations[0].animation.frames[0].primary_header.version, 1, "animation 0 frame 0 version was not 1")

    # Animation 0 Frame 0 Secondary Header
    check.equal(p.object.library.animations[0].animation.frames[0].frame.secondary_header.duration, 5, "animation 0 frame 0 duration was not 5")
    check.equal(p.object.library.animations[0].animation.frames[0].frame.secondary_header.data_length, 48, "animation 0 frame 0 data_length was not 48")

    # Animation 0 Frame 0 TLC States
    check.equal(p.object.library.animations[0].animation.frames[0].frame.tlc_states[0].state, [0x111]*16, "animation 0 frame 0 tlc 0 states were not all 0x1")
    check.equal(p.object.library.animations[0].animation.frames[0].frame.tlc_states[1].state, [0x222]*16, "animation 0 frame 0 tlc 1 states were not all 0x2")

    ##############################################

    # Animation 0 Frame 1 Primary Header in object
    check.equal(p.object.library.animations[0].animation.frames[1].primary_header.type.value, 0, "animation 0 frame 1 type was not 0")
    check.equal(p.object.library.animations[0].animation.frames[1].primary_header.type.name, "frame", "animation 0 frame 1 type was not \"frame\"")
    check.equal(p.object.library.animations[0].animation.frames[1].primary_header.version, 1, "animation 0 frame 1 version was not 1")

    # Animation 0 Frame 1 Secondary Header
    check.equal(p.object.library.animations[0].animation.frames[1].frame.secondary_header.duration, 5, "animation 0 frame 1 duration was not 5")
    check.equal(p.object.library.animations[0].animation.frames[1].frame.secondary_header.data_length, 48, "animation 0 frame 1 data_length was not 48")

    # Animation 0 Frame 1 TLC States
    check.equal(p.object.library.animations[0].animation.frames[1].frame.tlc_states[0].state, [0x333]*16, "animation 0 frame 1 tlc 0 states were not all 0x3")
    check.equal(p.object.library.animations[0].animation.frames[1].frame.tlc_states[1].state, [0x444]*16, "animation 0 frame 1 tlc 1 states were not all 0x4")

    ##############################################

    # Animation 0 Frame 2 Primary Header in object
    check.equal(p.object.library.animations[0].animation.frames[2].primary_header.type.value, 0, "animation 0 frame 2 type was not 0")
    check.equal(p.object.library.animations[0].animation.frames[2].primary_header.type.name, "frame", "animation 0 frame 2 type was not \"frame\"")
    check.equal(p.object.library.animations[0].animation.frames[2].primary_header.version, 1, "animation 0 frame 2 version was not 1")

    # Animation 0 Frame 2 Secondary Header
    check.equal(p.object.library.animations[0].animation.frames[2].frame.secondary_header.duration, 5, "animation 0 frame 2 duration was not 5")
    check.equal(p.object.library.animations[0].animation.frames[2].frame.secondary_header.data_length, 48, "animation 0 frame 2 data_length was not 48")

    # Animation 0 Frame 2 TLC States
    check.equal(p.object.library.animations[0].animation.frames[2].frame.tlc_states[0].state, [0x555]*16, "animation 0 frame 2 tlc 0 states were not all 0x5")
    check.equal(p.object.library.animations[0].animation.frames[2].frame.tlc_states[1].state, [0x666]*16, "animation 0 frame 2 tlc 1 states were not all 0x6")

    ##############################################

    # Animation 0 SHA256
    check.equal(
        p.object.library.animations[0].sha256,
        bytes.fromhex("2362 75D0 3729 2CAC 86E6 BFD2 E2BA 08AC 944F DF3A 5F72 D2D5 E3F7 1512 9EDB 0930"),
        "animation 0 sha256 was not: 2362 75D0 3729 2CAC 86E6 BFD2 E2BA 08AC 944F DF3A 5F72 D2D5 E3F7 1512 9EDB 0930"
    )

    ################################################################################################

    # Animation 1 Primary Header in parser
    check.equal(p.object.library.animations[1].primary_header.type.value, 1, "animation 1 type was not 1")
    check.equal(p.object.library.animations[1].primary_header.type.name, "animation", "animation 1 type was not \"animation\"")
    check.equal(p.object.library.animations[1].primary_header.version, 1, "animation 1 version was not 1")

    # Animation 1 Secondary Header
    check.equal(p.object.library.animations[1].animation.secondary_header.name, "Test" + "\0"*28, "animation 1 name was not \"Test\"")
    check.equal(p.object.library.animations[1].animation.secondary_header.time, 0x3E8, "animation 1 time was not 0x3E8")
    check.equal(p.object.library.animations[1].animation.secondary_header.tlc_count, 2, "animation 1 tlc_count was not 2")
    check.equal(p.object.library.animations[1].animation.secondary_header.frame_count, 3, "animation 1 frame_count was not 3")
    check.equal(p.object.library.animations[1].animation.secondary_header.data_length, 0xA6, "animation 1 data_length was not 0xA6")

    ##############################################

    # Animation 1 Frame 0 Primary Header in object
    check.equal(p.object.library.animations[1].animation.frames[0].primary_header.type.value, 0, "animation 1 frame 0 type was not 0")
    check.equal(p.object.library.animations[1].animation.frames[0].primary_header.type.name, "frame", "animation 1 frame 0 type was not \"frame\"")
    check.equal(p.object.library.animations[1].animation.frames[0].primary_header.version, 1, "animation 1 frame 0 version was not 1")

    # Animation 1 Frame 0 Secondary Header
    check.equal(p.object.library.animations[1].animation.frames[0].frame.secondary_header.duration, 5, "animation 1 frame 0 duration was not 5")
    check.equal(p.object.library.animations[1].animation.frames[0].frame.secondary_header.data_length, 48, "animation 1 frame 0 data_length was not 48")

    # Animation 1 Frame 0 TLC States
    check.equal(p.object.library.animations[1].animation.frames[0].frame.tlc_states[0].state, [0xAAA]*16, "animation 1 frame 0 tlc 0 states were not all 0xA")
    check.equal(p.object.library.animations[1].animation.frames[0].frame.tlc_states[1].state, [0xBBB]*16, "animation 1 frame 0 tlc 1 states were not all 0xB")

    ##############################################

    # Animation 1 Frame 1 Primary Header in object
    check.equal(p.object.library.animations[1].animation.frames[1].primary_header.type.value, 0, "animation 1 frame 1 type was not 0")
    check.equal(p.object.library.animations[1].animation.frames[1].primary_header.type.name, "frame", "animation 1 frame 1 type was not \"frame\"")
    check.equal(p.object.library.animations[1].animation.frames[1].primary_header.version, 1, "animation 1 frame 1 version was not 1")

    # Animation 1 Frame 1 Secondary Header
    check.equal(p.object.library.animations[1].animation.frames[1].frame.secondary_header.duration, 5, "animation 1 frame 1 duration was not 5")
    check.equal(p.object.library.animations[1].animation.frames[1].frame.secondary_header.data_length, 48, "animation 1 frame 1 data_length was not 48")

    # Animation 1 Frame 1 TLC States
    check.equal(p.object.library.animations[1].animation.frames[1].frame.tlc_states[0].state, [0xCCC]*16, "animation 1 frame 1 tlc 0 states were not all 0xC")
    check.equal(p.object.library.animations[1].animation.frames[1].frame.tlc_states[1].state, [0xDDD]*16, "animation 1 frame 1 tlc 1 states were not all 0xD")

    ##############################################

    # Animation 1 Frame 2 Primary Header in object
    check.equal(p.object.library.animations[1].animation.frames[2].primary_header.type.value, 0, "animation 1 frame 2 type was not 0")
    check.equal(p.object.library.animations[1].animation.frames[2].primary_header.type.name, "frame", "animation 1 frame 2 type was not \"frame\"")
    check.equal(p.object.library.animations[1].animation.frames[2].primary_header.version, 1, "animation 1 frame 2 version was not 1")

    # Animation 1 Frame 2 Secondary Header
    check.equal(p.object.library.animations[1].animation.frames[2].frame.secondary_header.duration, 5, "animation 1 frame 2 duration was not 5")
    check.equal(p.object.library.animations[1].animation.frames[2].frame.secondary_header.data_length, 48, "animation 1 frame 2 data_length was not 48")

    # Animation 1 Frame 2 TLC States
    check.equal(p.object.library.animations[1].animation.frames[2].frame.tlc_states[0].state, [0xEEE]*16, "animation 1 frame 2 tlc 0 states were not all 0xE")
    check.equal(p.object.library.animations[1].animation.frames[2].frame.tlc_states[1].state, [0xFFF]*16, "animation 1 frame 2 tlc 1 states were not all 0xF")

    ##############################################

    # Animation 1 SHA256
    check.equal(
        p.object.library.animations[1].sha256,
        bytes.fromhex("04CA 25AA B4F3 284D EB20 2589 A68E 4202 99D9 7EF3 A94E 872B B3C1 0D5A 00FB 3650"),
        "sha256 was not: 04CA 25AA B4F3 284D EB20 2589 A68E 4202 99D9 7EF3 A94E 872B B3C1 0D5A 00FB 3650"
    )

    ################################################################################################

    # Library SHA256
    check.equal(
        p.object.sha256,
        bytes.fromhex("4583 6DCB 46CF 226D 2100 B543 C5C9 9172 671C BECC A892 F214 26AC 1407 33D3 8535"),
        "sha256 was not: 4583 6DCB 46CF 226D 2100 B543 C5C9 9172 671C BECC A892 F214 26AC 1407 33D3 8535"
    )


def test_cube_file_v1():
    p = led_cube_data.Parser.from_file("./doc/file_specification/objects/cube_file/cube_file_v1.bin")

    # Cube File Primary Header in parser
    check.equal(p.primary_header.type.value, 3, "type was not 3")
    check.equal(p.primary_header.type.name, "file", "type was not \"file\"")
    check.equal(p.primary_header.version, 1, "version was not 1")

    # Cube File Primary Header in object
    check.equal(p.object.primary_header.type.value, p.primary_header.type.value, "Difference in Type value for parser primary header and object primary header")
    check.equal(p.object.primary_header.type.name, p.primary_header.type.name, "Difference in Type symbol for parser primary header and object primary header")
    check.equal(p.object.primary_header.version, p.primary_header.version, "Difference in Version for parser primary header and object primary header")

    ################################################################################################

    # Library Primary Header in parser
    check.equal(p.object.file.primary_header.type.value, 2, "type was not 2")
    check.equal(p.object.file.primary_header.type.name, "library", "type was not \"library\"")
    check.equal(p.object.file.primary_header.version, 1, "version was not 1")

    # Library Secondary Header
    check.equal(p.object.file.library.secondary_header.name, "Test Library" + "\0"*20, "name was not \"Test Library\"")
    check.equal(p.object.file.library.secondary_header.time, 0x3E8, "time was not 0x3E8")
    check.equal(p.object.file.library.secondary_header.animation_count, 2, "animation_count was not 2")
    check.equal(p.object.file.library.secondary_header.data_length, 0x1B6, "data_length was not 0x1B2")

    ##############################################

    # Animation 0 Primary Header in parser
    check.equal(p.object.file.library.animations[0].primary_header.type.value, 1, "animation 0 type was not 1")
    check.equal(p.object.file.library.animations[0].primary_header.type.name, "animation", "animation 0 type was not \"animation\"")
    check.equal(p.object.file.library.animations[0].primary_header.version, 1, "animation 0 version was not 1")

    # Animation 0 Secondary Header
    check.equal(p.object.file.library.animations[0].animation.secondary_header.name, "Test" + "\0"*28, "animation 0 name was not \"Test\"")
    check.equal(p.object.file.library.animations[0].animation.secondary_header.time, 0x3E8, "animation 0 time was not 0x3E8")
    check.equal(p.object.file.library.animations[0].animation.secondary_header.tlc_count, 2, "animation 0 tlc_count was not 2")
    check.equal(p.object.file.library.animations[0].animation.secondary_header.frame_count, 3, "animation 0 frame_count was not 3")
    check.equal(p.object.file.library.animations[0].animation.secondary_header.data_length, 0xA6, "animation 0 data_length was not 0xA6")

    #####################

    # Animation 0 Frame 0 Primary Header in object
    check.equal(p.object.file.library.animations[0].animation.frames[0].primary_header.type.value, 0, "animation 0 frame 0 type was not 0")
    check.equal(p.object.file.library.animations[0].animation.frames[0].primary_header.type.name, "frame", "animation 0 frame 0 type was not \"frame\"")
    check.equal(p.object.file.library.animations[0].animation.frames[0].primary_header.version, 1, "animation 0 frame 0 version was not 1")

    # Animation 0 Frame 0 Secondary Header
    check.equal(p.object.file.library.animations[0].animation.frames[0].frame.secondary_header.duration, 5, "animation 0 frame 0 duration was not 5")
    check.equal(p.object.file.library.animations[0].animation.frames[0].frame.secondary_header.data_length, 48, "animation 0 frame 0 data_length was not 48")

    # Animation 0 Frame 0 TLC States
    check.equal(p.object.file.library.animations[0].animation.frames[0].frame.tlc_states[0].state, [0x111]*16, "animation 0 frame 0 tlc 0 states were not all 0x1")
    check.equal(p.object.file.library.animations[0].animation.frames[0].frame.tlc_states[1].state, [0x222]*16, "animation 0 frame 0 tlc 1 states were not all 0x2")

    #####################

    # Animation 0 Frame 1 Primary Header in object
    check.equal(p.object.file.library.animations[0].animation.frames[1].primary_header.type.value, 0, "animation 0 frame 1 type was not 0")
    check.equal(p.object.file.library.animations[0].animation.frames[1].primary_header.type.name, "frame", "animation 0 frame 1 type was not \"frame\"")
    check.equal(p.object.file.library.animations[0].animation.frames[1].primary_header.version, 1, "animation 0 frame 1 version was not 1")

    # Animation 0 Frame 1 Secondary Header
    check.equal(p.object.file.library.animations[0].animation.frames[1].frame.secondary_header.duration, 5, "animation 0 frame 1 duration was not 5")
    check.equal(p.object.file.library.animations[0].animation.frames[1].frame.secondary_header.data_length, 48, "animation 0 frame 1 data_length was not 48")

    # Animation 0 Frame 1 TLC States
    check.equal(p.object.file.library.animations[0].animation.frames[1].frame.tlc_states[0].state, [0x333]*16, "animation 0 frame 1 tlc 0 states were not all 0x3")
    check.equal(p.object.file.library.animations[0].animation.frames[1].frame.tlc_states[1].state, [0x444]*16, "animation 0 frame 1 tlc 1 states were not all 0x4")

    #####################

    # Animation 0 Frame 2 Primary Header in object
    check.equal(p.object.file.library.animations[0].animation.frames[2].primary_header.type.value, 0, "animation 0 frame 2 type was not 0")
    check.equal(p.object.file.library.animations[0].animation.frames[2].primary_header.type.name, "frame", "animation 0 frame 2 type was not \"frame\"")
    check.equal(p.object.file.library.animations[0].animation.frames[2].primary_header.version, 1, "animation 0 frame 2 version was not 1")

    # Animation 0 Frame 2 Secondary Header
    check.equal(p.object.file.library.animations[0].animation.frames[2].frame.secondary_header.duration, 5, "animation 0 frame 2 duration was not 5")
    check.equal(p.object.file.library.animations[0].animation.frames[2].frame.secondary_header.data_length, 48, "animation 0 frame 2 data_length was not 48")

    # Animation 0 Frame 2 TLC States
    check.equal(p.object.file.library.animations[0].animation.frames[2].frame.tlc_states[0].state, [0x555]*16, "animation 0 frame 2 tlc 0 states were not all 0x5")
    check.equal(p.object.file.library.animations[0].animation.frames[2].frame.tlc_states[1].state, [0x666]*16, "animation 0 frame 2 tlc 1 states were not all 0x6")

    #####################

    # Animation 0 SHA256
    check.equal(
        p.object.file.library.animations[0].sha256,
        bytes.fromhex("2362 75D0 3729 2CAC 86E6 BFD2 E2BA 08AC 944F DF3A 5F72 D2D5 E3F7 1512 9EDB 0930"),
        "animation 0 sha256 was not: 2362 75D0 3729 2CAC 86E6 BFD2 E2BA 08AC 944F DF3A 5F72 D2D5 E3F7 1512 9EDB 0930"
    )

    ##############################################

    # Animation 1 Primary Header in parser
    check.equal(p.object.file.library.animations[1].primary_header.type.value, 1, "animation 1 type was not 1")
    check.equal(p.object.file.library.animations[1].primary_header.type.name, "animation", "animation 1 type was not \"animation\"")
    check.equal(p.object.file.library.animations[1].primary_header.version, 1, "animation 1 version was not 1")

    # Animation 1 Secondary Header
    check.equal(p.object.file.library.animations[1].animation.secondary_header.name, "Test" + "\0"*28, "animation 1 name was not \"Test\"")
    check.equal(p.object.file.library.animations[1].animation.secondary_header.time, 0x3E8, "animation 1 time was not 0x3E8")
    check.equal(p.object.file.library.animations[1].animation.secondary_header.tlc_count, 2, "animation 1 tlc_count was not 2")
    check.equal(p.object.file.library.animations[1].animation.secondary_header.frame_count, 3, "animation 1 frame_count was not 3")
    check.equal(p.object.file.library.animations[1].animation.secondary_header.data_length, 0xA6, "animation 1 data_length was not 0xA6")

    #####################

    # Animation 1 Frame 0 Primary Header in object
    check.equal(p.object.file.library.animations[1].animation.frames[0].primary_header.type.value, 0, "animation 1 frame 0 type was not 0")
    check.equal(p.object.file.library.animations[1].animation.frames[0].primary_header.type.name, "frame", "animation 1 frame 0 type was not \"frame\"")
    check.equal(p.object.file.library.animations[1].animation.frames[0].primary_header.version, 1, "animation 1 frame 0 version was not 1")

    # Animation 1 Frame 0 Secondary Header
    check.equal(p.object.file.library.animations[1].animation.frames[0].frame.secondary_header.duration, 5, "animation 1 frame 0 duration was not 5")
    check.equal(p.object.file.library.animations[1].animation.frames[0].frame.secondary_header.data_length, 48, "animation 1 frame 0 data_length was not 48")

    # Animation 1 Frame 0 TLC States
    check.equal(p.object.file.library.animations[1].animation.frames[0].frame.tlc_states[0].state, [0xAAA]*16, "animation 1 frame 0 tlc 0 states were not all 0xA")
    check.equal(p.object.file.library.animations[1].animation.frames[0].frame.tlc_states[1].state, [0xBBB]*16, "animation 1 frame 0 tlc 1 states were not all 0xB")

    #####################

    # Animation 1 Frame 1 Primary Header in object
    check.equal(p.object.file.library.animations[1].animation.frames[1].primary_header.type.value, 0, "animation 1 frame 1 type was not 0")
    check.equal(p.object.file.library.animations[1].animation.frames[1].primary_header.type.name, "frame", "animation 1 frame 1 type was not \"frame\"")
    check.equal(p.object.file.library.animations[1].animation.frames[1].primary_header.version, 1, "animation 1 frame 1 version was not 1")

    # Animation 1 Frame 1 Secondary Header
    check.equal(p.object.file.library.animations[1].animation.frames[1].frame.secondary_header.duration, 5, "animation 1 frame 1 duration was not 5")
    check.equal(p.object.file.library.animations[1].animation.frames[1].frame.secondary_header.data_length, 48, "animation 1 frame 1 data_length was not 48")

    # Animation 1 Frame 1 TLC States
    check.equal(p.object.file.library.animations[1].animation.frames[1].frame.tlc_states[0].state, [0xCCC]*16, "animation 1 frame 1 tlc 0 states were not all 0xC")
    check.equal(p.object.file.library.animations[1].animation.frames[1].frame.tlc_states[1].state, [0xDDD]*16, "animation 1 frame 1 tlc 1 states were not all 0xD")

    #####################

    # Animation 1 Frame 2 Primary Header in object
    check.equal(p.object.file.library.animations[1].animation.frames[2].primary_header.type.value, 0, "animation 1 frame 2 type was not 0")
    check.equal(p.object.file.library.animations[1].animation.frames[2].primary_header.type.name, "frame", "animation 1 frame 2 type was not \"frame\"")
    check.equal(p.object.file.library.animations[1].animation.frames[2].primary_header.version, 1, "animation 1 frame 2 version was not 1")

    # Animation 1 Frame 2 Secondary Header
    check.equal(p.object.file.library.animations[1].animation.frames[2].frame.secondary_header.duration, 5, "animation 1 frame 2 duration was not 5")
    check.equal(p.object.file.library.animations[1].animation.frames[2].frame.secondary_header.data_length, 48, "animation 1 frame 2 data_length was not 48")

    # Animation 1 Frame 2 TLC States
    check.equal(p.object.file.library.animations[1].animation.frames[2].frame.tlc_states[0].state, [0xEEE]*16, "animation 1 frame 2 tlc 0 states were not all 0xE")
    check.equal(p.object.file.library.animations[1].animation.frames[2].frame.tlc_states[1].state, [0xFFF]*16, "animation 1 frame 2 tlc 1 states were not all 0xF")

    #####################

    # Animation 1 SHA256
    check.equal(
        p.object.file.library.animations[1].sha256,
        bytes.fromhex("04CA 25AA B4F3 284D EB20 2589 A68E 4202 99D9 7EF3 A94E 872B B3C1 0D5A 00FB 3650"),
        "sha256 was not: 04CA 25AA B4F3 284D EB20 2589 A68E 4202 99D9 7EF3 A94E 872B B3C1 0D5A 00FB 3650"
    )

    ################################################################################################

    # Library SHA256
    check.equal(
        p.object.file.sha256,
        bytes.fromhex("4583 6DCB 46CF 226D 2100 B543 C5C9 9172 671C BECC A892 F214 26AC 1407 33D3 8535"),
        "sha256 was not: 4583 6DCB 46CF 226D 2100 B543 C5C9 9172 671C BECC A892 F214 26AC 1407 33D3 8535"
    )
