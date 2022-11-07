from led_cube_data import assemblers


def test_frame_v1():
    with open("./doc/file_specification/objects/frame/frame_v1.bin", "rb") as f:
        data = f.read()

    obj = assemblers.FrameV1(duration=5, tlc_states=[[0xAAA]*16, [0xBBB]*16])

    assert obj.generate() == data, "frame_v1 assembler did not build the same data as the frame_v1.bin binary"


def test_animation_v1():
    with open("./doc/file_specification/objects/animation/animation_v1.bin", "rb") as f:
        data = f.read()

    obj = assemblers.AnimationV1(
        name="Test",
        timestamp=0x3E8,
        tlc_count=2,
        frame_count=3,
        frames=[
            assemblers.FrameV1(duration=5, tlc_states=[[0xAAA]*16, [0xBBB]*16]),
            assemblers.FrameV1(duration=5, tlc_states=[[0xCCC]*16, [0xDDD]*16]),
            assemblers.FrameV1(duration=5, tlc_states=[[0xEEE]*16, [0xFFF]*16]),
        ]
        )

    assert obj.generate() == data, "animation_v1 assembler did not build the same data as the animation_v1.bin binary"


def test_library_v1():
    with open("./doc/file_specification/objects/library/library_v1.bin", "rb") as f:
        data = f.read()

    obj = assemblers.LibraryV1(
        name="Test Library",
        timestamp=0x3E8,
        animation_count=2,
        animations=[
            assemblers.AnimationV1(name="Test", timestamp=0x3E8, tlc_count=2, frame_count=3, frames=[
                assemblers.FrameV1(duration=5, tlc_states=[[0x111]*16, [0x222]*16]),
                assemblers.FrameV1(duration=5, tlc_states=[[0x333]*16, [0x444]*16]),
                assemblers.FrameV1(duration=5, tlc_states=[[0x555]*16, [0x666]*16]),
            ]),
            assemblers.AnimationV1(name="Test", timestamp=0x3E8, tlc_count=2, frame_count=3, frames=[
                assemblers.FrameV1(duration=5, tlc_states=[[0xAAA]*16, [0xBBB]*16]),
                assemblers.FrameV1(duration=5, tlc_states=[[0xCCC]*16, [0xDDD]*16]),
                assemblers.FrameV1(duration=5, tlc_states=[[0xEEE]*16, [0xFFF]*16]),
            ]),
        ]
        )

    assert obj.generate() == data, "library_v1 assembler did not build the same data as the library_v1.bin binary"


def test_cube_file_v1():
    with open("./doc/file_specification/objects/cube_file/cube_file_v1.bin", "rb") as f:
        data = f.read()

    obj = assemblers.CubeFileV1(
        library=assemblers.LibraryV1(
            name="Test Library",
            timestamp=0x3E8,
            animation_count=2,
            animations=[
                assemblers.AnimationV1(name="Test", timestamp=0x3E8, tlc_count=2, frame_count=3, frames=[
                    assemblers.FrameV1(duration=5, tlc_states=[[0x111]*16, [0x222]*16]),
                    assemblers.FrameV1(duration=5, tlc_states=[[0x333]*16, [0x444]*16]),
                    assemblers.FrameV1(duration=5, tlc_states=[[0x555]*16, [0x666]*16]),
                ]),
                assemblers.AnimationV1(name="Test", timestamp=0x3E8, tlc_count=2, frame_count=3, frames=[
                    assemblers.FrameV1(duration=5, tlc_states=[[0xAAA]*16, [0xBBB]*16]),
                    assemblers.FrameV1(duration=5, tlc_states=[[0xCCC]*16, [0xDDD]*16]),
                    assemblers.FrameV1(duration=5, tlc_states=[[0xEEE]*16, [0xFFF]*16]),
                ]),
            ]
            )
        )

    assert obj.generate() == data, "cube_file_v1 assembler did not build the same data as the cube_file_v1.bin binary"
