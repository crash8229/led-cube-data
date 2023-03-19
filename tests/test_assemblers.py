from led_cube_data import assembler

from pytest_check import check  # type: ignore[import]


def test_frame_v1():
    with open("./doc/file_specification/objects/frame/frame_v1.bin", "rb") as f:
        data = f.read()

    obj = assembler.FrameV1(
        duration=5, tlc_states=[[0xAAA] * 16, [0xBBB] * 16, [0xCCC] * 16, [0xDDD] * 16]
    )

    check.equal(
        obj.generate(), data
    ), "frame_v1 assembler did not build the same data as the frame_v1.bin binary"

    check.equal(
        len(data),
        len(obj),
        "The size of the of generated binary does not equal the size of the test binary",
    )


def test_animation_v1():
    with open("./doc/file_specification/objects/animation/animation_v1.bin", "rb") as f:
        data = f.read()

    obj = assembler.AnimationV1(
        name="Test",
        timestamp=0x3E8,
        frames=[
            assembler.FrameV1(
                duration=5,
                tlc_states=[[0xAAA] * 16, [0xBBB] * 16, [0xCCC] * 16, [0xDDD] * 16],
            ),
            assembler.FrameV1(
                duration=5,
                tlc_states=[[0xEEE] * 16, [0xFFF] * 16, [0x000] * 16, [0x111] * 16],
            ),
        ],
    )

    check.equal(
        obj.generate(), data
    ), "animation_v1 assembler did not build the same data as the animation_v1.bin binary"

    check.equal(
        len(data),
        len(obj),
        "The size of the of generated binary does not equal the size of the test binary",
    )


def test_library_v1():
    with open("./doc/file_specification/objects/library/library_v1.bin", "rb") as f:
        data = f.read()

    obj = assembler.LibraryV1(
        name="Test Library",
        timestamp=0x3E8,
        x_size=4,
        y_size=5,
        z_size=2,
        tlc_count=2,
        animations=[
            assembler.AnimationV1(
                name="Test",
                timestamp=0x3E8,
                frames=[
                    assembler.FrameV1(
                        duration=5,
                        tlc_states=[
                            [0xAAA] * 16,
                            [0xBBB] * 16,
                            [0xCCC] * 16,
                            [0xDDD] * 16,
                        ],
                    ),
                    assembler.FrameV1(
                        duration=5,
                        tlc_states=[
                            [0xEEE] * 16,
                            [0xFFF] * 16,
                            [0x000] * 16,
                            [0x111] * 16,
                        ],
                    ),
                ],
            ),
            assembler.AnimationV1(
                name="Test2",
                timestamp=0x3E8,
                frames=[
                    assembler.FrameV1(
                        duration=5,
                        tlc_states=[
                            [0x222] * 16,
                            [0x333] * 16,
                            [0x444] * 16,
                            [0x555] * 16,
                        ],
                    ),
                    assembler.FrameV1(
                        duration=5,
                        tlc_states=[
                            [0x666] * 16,
                            [0x777] * 16,
                            [0x888] * 16,
                            [0x999] * 16,
                        ],
                    ),
                ],
            ),
        ],
    )

    check.equal(
        obj.generate(), data
    ), "library_v1 assembler did not build the same data as the library_v1.bin binary"

    check.equal(
        len(data),
        len(obj),
        "The size of the of generated binary does not equal the size of the test binary",
    )


def test_cube_file_v1():
    with open("./doc/file_specification/objects/cube_file/cube_file_v1.bin", "rb") as f:
        data = f.read()

    obj = assembler.CubeFileV1(
        assembler.LibraryV1(
            name="Test Library",
            timestamp=0x3E8,
            x_size=4,
            y_size=5,
            z_size=2,
            tlc_count=2,
            animations=[
                assembler.AnimationV1(
                    name="Test",
                    timestamp=0x3E8,
                    frames=[
                        assembler.FrameV1(
                            duration=5,
                            tlc_states=[
                                [0xAAA] * 16,
                                [0xBBB] * 16,
                                [0xCCC] * 16,
                                [0xDDD] * 16,
                            ],
                        ),
                        assembler.FrameV1(
                            duration=5,
                            tlc_states=[
                                [0xEEE] * 16,
                                [0xFFF] * 16,
                                [0x000] * 16,
                                [0x111] * 16,
                            ],
                        ),
                    ],
                ),
                assembler.AnimationV1(
                    name="Test2",
                    timestamp=0x3E8,
                    frames=[
                        assembler.FrameV1(
                            duration=5,
                            tlc_states=[
                                [0x222] * 16,
                                [0x333] * 16,
                                [0x444] * 16,
                                [0x555] * 16,
                            ],
                        ),
                        assembler.FrameV1(
                            duration=5,
                            tlc_states=[
                                [0x666] * 16,
                                [0x777] * 16,
                                [0x888] * 16,
                                [0x999] * 16,
                            ],
                        ),
                    ],
                ),
            ],
        )
    )

    check.equal(
        obj.generate(), data
    ), "cube_file_v1 assembler did not build the same data as the cube_file_v1.bin binary"

    check.equal(
        len(data),
        len(obj),
        "The size of the of generated binary does not equal the size of the test binary",
    )
