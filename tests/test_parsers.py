import led_cube_data
from led_cube_data.parser import frame, animation, library

import pytest_check as check  # type: ignore[import]

from hashlib import sha256
from struct import Struct
from typing import List, Dict, Any


def null_terminated_string(chars: str, str_length: int = 32) -> str:
    return chars + "\0" * max(0, (str_length - len(chars)))


def check_frame_v1_data(
    obj: frame.Frame, duration: int, data_length: int, tlc_states: List[int]
):
    frame_v1: frame.frame_v1.FrameV1 = obj.frame  # noqa

    # Frame Primary Header in object
    check.equal(obj.primary_header.type.value, 0, "type was not 0")
    check.equal(obj.primary_header.type.name, "frame", 'type was not "frame"')
    check.equal(obj.primary_header.version, 1, "version was not 1")

    # Frame Secondary Header
    check.equal(
        frame_v1.secondary_header.duration, duration, f"duration was not {duration}"
    )
    check.equal(
        frame_v1.secondary_header.data_length,
        data_length,
        f"data_length was not {data_length}",
    )

    # Frame TLC States
    for i in range(len(tlc_states)):
        state = tlc_states[i]
        check.equal(
            frame_v1.tlc_states[i].state,
            [state] * 16,
            f"tlc {i} states were not all 0x{state:X}",
        )


def check_animation_v1_data(
    obj: animation.Animation,
    animation_idx: int,  # Needed for determining the location of the animation inside other structures
    name: str,
    time: int,
    frame_count: int,
    data_length: int,
    frame_test_data: List[Dict[str, Any]],
    seek_start: int,
):
    animation_v1: animation.animation_v1.AnimationV1 = obj.animation  # noqa

    # Animation Primary Header in object
    check.equal(obj.primary_header.type.value, 1, "type was not 1")
    check.equal(obj.primary_header.type.name, "animation", 'type was not "animation"')
    check.equal(obj.primary_header.version, 1, "version was not 1")

    ################################################################################################

    # SHA256
    io = obj._io._io  # noqa
    pos = io.tell()
    io.seek(seek_start)
    if io.read(1) == bytes([2]):
        offset = 87
        io.seek(offset - 1, 1)
        unpacker = Struct(">I")
        for i in range(animation_idx):
            io.seek(76, 1)
            io.seek(unpacker.unpack(io.read(4))[0], 1)
    else:
        io.seek(seek_start)
    io.seek(34, 1)
    # Number of bytes in the secondary header plus data_length
    checksum = sha256(io.read(46 + animation_v1.secondary_header.data_length)).digest()
    io.seek(pos)
    check.equal(obj.sha256, checksum, "Failed sha256 check")

    ################################################################################################

    # Animation Secondary Header
    check.equal(
        animation_v1.secondary_header.name,
        null_terminated_string(name, 32),
        f'name was not "{name}"',
    )
    check.equal(animation_v1.secondary_header.time, time, f"time was not 0x{time:X}")
    check.equal(
        animation_v1.secondary_header.frame_count,
        frame_count,
        f"frame_count was not {frame_count}",
    )
    check.equal(
        animation_v1.secondary_header.data_length,
        data_length,
        f"data_length was not {data_length}",
    )

    ################################################################################################

    # Check frame data
    for i in range(animation_v1.secondary_header.frame_count):
        check_frame_v1_data(obj=animation_v1.frames[i], **frame_test_data[i])


def check_library_v1_data(
    obj: library.Library,
    library_idx: int,  # Needed for determining the location of the library inside other structures
    name: str,
    time: int,
    x_size: int,
    y_size: int,
    z_size: int,
    tlc_count: int,
    animation_count: int,
    data_length: int,
    animation_test_data: List[Dict[str, Any]],
):
    library_v1: library.library_v1.LibraryV1 = obj.library

    # Library Primary Header in object
    check.equal(obj.primary_header.type.value, 2, "type was not 2")
    check.equal(obj.primary_header.type.name, "library", 'type was not "library"')
    check.equal(obj.primary_header.version, 1, "version was not 1")

    ################################################################################################

    # SHA256
    io = obj._io._io  # noqa
    pos = io.tell()
    io.seek(0)
    if io.read(1) == bytes([3]):
        offset = 2
        io.seek(offset)
        unpacker = Struct(">Q")
        for i in range(library_idx):
            io.seek(79, 1)
            io.seek(unpacker.unpack(io.read(8))[0], 1)
    else:
        io.seek(0)
    io.seek(34, 1)
    # Number of bytes in the secondary header plus data_length
    checksum = sha256(io.read(53 + library_v1.secondary_header.data_length)).digest()
    io.seek(pos)
    check.equal(obj.sha256, checksum, "Failed sha256 check")

    ################################################################################################

    # Library Secondary Header
    check.equal(
        library_v1.secondary_header.name,
        null_terminated_string(name, 32),
        f'name was not "{name}"',
    )
    check.equal(library_v1.secondary_header.time, time, f"time was not 0x{time:X}")
    check.equal(library_v1.secondary_header.x_size, x_size, f"x_size was not {x_size}")
    check.equal(library_v1.secondary_header.y_size, y_size, f"y_size was not {y_size}")
    check.equal(library_v1.secondary_header.z_size, z_size, f"z_size was not {z_size}")
    check.equal(
        library_v1.secondary_header.tlc_count,
        tlc_count,
        f"tlc_count was not {tlc_count}",
    )
    check.equal(
        library_v1.secondary_header.animation_count,
        animation_count,
        f"animation_count was not {animation_count}",
    )
    check.equal(
        library_v1.secondary_header.data_length,
        data_length,
        f"data_length was not {data_length}",
    )

    ################################################################################################

    # Check animation data
    for i in range(library_v1.secondary_header.animation_count):
        check_animation_v1_data(
            obj=library_v1.animations[i], animation_idx=i, **animation_test_data[i]
        )


def test_frame_v1():
    p = led_cube_data.Parser.from_file(
        "./doc/file_specification/objects/frame/frame_v1.bin"
    )

    # Frame Primary Header in parser
    check.equal(p.primary_header.type.value, 0, "type was not 0")
    check.equal(p.primary_header.type.name, "frame", 'type was not "frame"')
    check.equal(p.primary_header.version, 1, "version was not 1")

    # Verify that the amount of data after the secondary header matches the data length
    io = p.object.frame._io._io  # noqa
    pos = io.tell()
    io.seek(6)
    length = len(io.read())
    io.seek(pos)
    check.equal(
        p.object.frame.secondary_header.data_length,
        length,
        "Amount of data after secondary header does not equal data_length",
    )

    # Check the rest of the frame
    check_frame_v1_data(
        obj=p.object,
        duration=5,
        data_length=96,
        tlc_states=[0xAAA, 0xBBB, 0xCCC, 0xDDD],
    )


def test_animation_v1():
    p = led_cube_data.Parser.from_file(
        "./doc/file_specification/objects/animation/animation_v1.bin"
    )

    # Animation Primary Header in parser
    check.equal(p.primary_header.type.value, 1, "type was not 1")
    check.equal(p.primary_header.type.name, "animation", 'type was not "animation"')
    check.equal(p.primary_header.version, 1, "version was not 1")

    # Verify that the amount of data after the secondary header matches the data length
    io = p.object.animation._io._io
    pos = io.tell()
    io.seek(80)
    length = len(io.read())
    io.seek(pos)
    check.equal(
        p.object.animation.secondary_header.data_length,
        length,
        "Amount of data after secondary header does not equal data_length",
    )

    # Check the rest of the animation data
    frame_test_data = [
        {"duration": 5, "data_length": 96, "tlc_states": [0xAAA, 0xBBB, 0xCCC, 0xDDD]},
        {"duration": 5, "data_length": 96, "tlc_states": [0xEEE, 0xFFF, 0x000, 0x111]},
    ]
    check_animation_v1_data(
        obj=p.object,
        animation_idx=0,
        name="Test",
        time=0x3E8,
        frame_count=2,
        data_length=204,
        frame_test_data=frame_test_data,
        seek_start=0,
    )


def test_library_v1():
    p = led_cube_data.Parser.from_file(
        "./doc/file_specification/objects/library/library_v1.bin"
    )

    # Library Primary Header in parser
    check.equal(p.primary_header.type.value, 2, "type was not 2")
    check.equal(p.primary_header.type.name, "library", 'type was not "library"')
    check.equal(p.primary_header.version, 1, "version was not 1")

    # Verify that the amount of data after the secondary header matches the data length
    io = p.object.library._io._io
    pos = io.tell()
    io.seek(87)
    length = len(io.read())
    io.seek(pos)
    check.equal(
        p.object.library.secondary_header.data_length,
        length,
        "Amount of data after secondary header does not equal data_length",
    )

    # Check the rest of the library data
    animation_test_data = [
        {
            "name": "Test",
            "time": 0x3E8,
            "frame_count": 2,
            "data_length": 204,
            "frame_test_data": [
                {
                    "duration": 5,
                    "data_length": 96,
                    "tlc_states": [0xAAA, 0xBBB, 0xCCC, 0xDDD],
                },
                {
                    "duration": 5,
                    "data_length": 96,
                    "tlc_states": [0xEEE, 0xFFF, 0x000, 0x111],
                },
            ],
            "seek_start": 0,
        },
        {
            "name": "Test2",
            "time": 0x3E8,
            "frame_count": 2,
            "data_length": 204,
            "frame_test_data": [
                {
                    "duration": 5,
                    "data_length": 96,
                    "tlc_states": [0x222, 0x333, 0x444, 0x555],
                },
                {
                    "duration": 5,
                    "data_length": 96,
                    "tlc_states": [0x666, 0x777, 0x888, 0x999],
                },
            ],
            "seek_start": 0,
        },
    ]
    check_library_v1_data(
        obj=p.object,
        library_idx=0,
        name="Test Library",
        time=0x3E8,
        x_size=4,
        y_size=5,
        z_size=2,
        tlc_count=2,
        animation_count=2,
        data_length=568,
        animation_test_data=animation_test_data,
    )


def test_cube_file_v1():
    p = led_cube_data.Parser.from_file(
        "./doc/file_specification/objects/cube_file/cube_file_v1.bin"
    )

    # Cube File Primary Header in parser
    check.equal(p.primary_header.type.value, 3, "type was not 3")
    check.equal(p.primary_header.type.name, "file", 'type was not "file"')
    check.equal(p.primary_header.version, 1, "version was not 1")

    check.equal(p.object.primary_header.type.value, 3, "type was not 3")
    check.equal(p.object.primary_header.type.name, "file", 'type was not "file"')
    check.equal(p.object.primary_header.version, 1, "version was not 1")

    # Check the rest of the cube file data
    animation_test_data = [
        {
            "name": "Test",
            "time": 0x3E8,
            "frame_count": 2,
            "data_length": 204,
            "frame_test_data": [
                {
                    "duration": 5,
                    "data_length": 96,
                    "tlc_states": [0xAAA, 0xBBB, 0xCCC, 0xDDD],
                },
                {
                    "duration": 5,
                    "data_length": 96,
                    "tlc_states": [0xEEE, 0xFFF, 0x000, 0x111],
                },
            ],
            "seek_start": 2,
        },
        {
            "name": "Test2",
            "time": 0x3E8,
            "frame_count": 2,
            "data_length": 204,
            "frame_test_data": [
                {
                    "duration": 5,
                    "data_length": 96,
                    "tlc_states": [0x222, 0x333, 0x444, 0x555],
                },
                {
                    "duration": 5,
                    "data_length": 96,
                    "tlc_states": [0x666, 0x777, 0x888, 0x999],
                },
            ],
            "seek_start": 2,
        },
    ]
    check_library_v1_data(
        obj=p.object.file,
        library_idx=0,
        name="Test Library",
        time=0x3E8,
        x_size=4,
        y_size=5,
        z_size=2,
        tlc_count=2,
        animation_count=2,
        data_length=568,
        animation_test_data=animation_test_data,
    )
