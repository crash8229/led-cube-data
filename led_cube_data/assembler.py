from copy import deepcopy
from hashlib import sha256
from typing import Sequence, Dict, Any

from construct import SizeofError, Struct

from led_cube_data import serializer


class BaseAssembler:
    def __init__(self, serializer_struct: Struct) -> None:
        self._populated_data: Dict[str, Any] = dict()
        self._serializer: Struct = serializer_struct

    @property
    def populated_data(self) -> Dict[str, Any]:
        return deepcopy(self._populated_data)

    def generate(self) -> bytes:
        try:
            return self._serializer.build(self._populated_data)
        except KeyError:
            raise ValueError("Data was not populated!")

    def __len__(self) -> int:
        raise NotImplementedError

    @staticmethod
    def template() -> Dict[str, Any]:
        raise NotImplementedError

    def populate(self, *args, **kwargs) -> None:
        raise NotImplementedError


#### Frames ####################################################################
class Frame(BaseAssembler):  # noqa
    def __init__(self) -> None:
        super().__init__(serializer.frame_frame)


class FrameV1(Frame):
    def __init__(self, duration: int, tlc_states: Sequence[Sequence[int]]) -> None:
        super().__init__()
        self.populate(duration, tlc_states)

    def populate(self, duration: int, tlc_states: Sequence[Sequence[int]]) -> None:
        data = self.template()
        data["frame"]["secondary_header"]["duration"] = duration
        data["frame"]["secondary_header"]["data_length"] = (
            len(tlc_states) * serializer.frame_v1_tlc.sizeof()
        )
        data["frame"]["tlc_states"] = [{"state": s} for s in tlc_states]

        self._populated_data = data

    def __len__(self) -> int:
        try:
            return (
                serializer.primary_header_primary_header.sizeof()
                + serializer.frame_v1_secondary_header.sizeof()
                + self._populated_data["frame"]["secondary_header"]["data_length"]
            )
        except (SizeofError, KeyError):
            raise ValueError("Data was not populated!")

    @staticmethod
    def template() -> Dict[str, Any]:
        return {
            "primary_header": {"type": "frame", "version": 1},
            "frame": {
                "secondary_header": {"duration": None, "data_length": None},
                "tlc_states": None,
            },
        }


#### Animations ################################################################
class Animation(BaseAssembler):  # noqa
    def __init__(self) -> None:
        super().__init__(serializer.animation_animation)


class AnimationV1(Animation):
    def __init__(
        self,
        name: str,
        timestamp: int,
        frames: Sequence[Frame],
    ) -> None:
        super().__init__()
        self.populate(name, timestamp, frames)

    def populate(
        self,
        name: str,
        timestamp: int,
        frames: Sequence[Frame],
    ) -> None:
        data = AnimationV1.template()
        data["animation"]["secondary_header"]["name"] = name
        data["animation"]["secondary_header"]["time"] = timestamp
        data["animation"]["secondary_header"]["frame_count"] = len(frames)

        # Calculate data length
        data["animation"]["secondary_header"]["data_length"] = sum(
            (len(fr) for fr in frames)
        )

        # Create frame data
        data["animation"]["frames"] = [f.populated_data for f in frames]

        # Generate Checksum
        data["sha256"] = sha256(
            serializer.animation_v1_animation_v1.build(data["animation"])
        ).digest()

        self._populated_data = data

    def __len__(self) -> int:
        try:
            return (
                serializer.primary_header_primary_header.sizeof()
                + len(self._populated_data["sha256"])
                + serializer.animation_v1_secondary_header.sizeof()
                + self._populated_data["animation"]["secondary_header"]["data_length"]
            )
        except (SizeofError, KeyError):
            raise ValueError("Data was not populated!")

    @staticmethod
    def template() -> Dict[str, Any]:
        return {
            "primary_header": {"type": "animation", "version": 1},
            "sha256": None,
            "animation": {
                "secondary_header": {
                    "name": None,
                    "time": None,
                    "frame_count": None,
                    "data_length": None,
                },
                "frames": None,
            },
        }


#### Libraries #################################################################
class Library(BaseAssembler):  # noqa
    def __init__(self) -> None:
        super().__init__(serializer.library_library)


class LibraryV1(Library):
    def __init__(
        self,
        name: str,
        timestamp: int,
        x_size: int,
        y_size: int,
        z_size: int,
        tlc_count: int,
        animations: Sequence[Animation],
    ) -> None:
        super().__init__()
        self.populate(name, timestamp, x_size, y_size, z_size, tlc_count, animations)

    def populate(
        self,
        name: str,
        timestamp: int,
        x_size: int,
        y_size: int,
        z_size: int,
        tlc_count: int,
        animations: Sequence[Animation],
    ) -> None:
        data = LibraryV1.template()
        data["library"]["secondary_header"]["name"] = name
        data["library"]["secondary_header"]["time"] = timestamp
        data["library"]["secondary_header"]["x_size"] = x_size
        data["library"]["secondary_header"]["y_size"] = y_size
        data["library"]["secondary_header"]["z_size"] = z_size
        data["library"]["secondary_header"]["tlc_count"] = tlc_count
        data["library"]["secondary_header"]["animation_count"] = len(animations)

        # Calculate data length
        data["library"]["secondary_header"]["data_length"] = sum(
            (len(ani) for ani in animations)
        )

        # Create frame data
        data["library"]["animations"] = [ani.populated_data for ani in animations]

        # Generate CRC
        data["sha256"] = sha256(
            serializer.library_v1_library_v1.build(data["library"])
        ).digest()

        self._populated_data = data

    def __len__(self) -> int:
        try:
            return (
                serializer.primary_header_primary_header.sizeof()
                + len(self._populated_data["sha256"])
                + serializer.library_v1_secondary_header.sizeof()
                + self._populated_data["library"]["secondary_header"]["data_length"]
            )
        except (SizeofError, KeyError):
            raise ValueError("Data was not populated!")

    @staticmethod
    def template() -> Dict[str, Any]:
        return {
            "primary_header": {"type": "library", "version": 1},
            "sha256": None,
            "library": {
                "secondary_header": {
                    "name": None,
                    "time": None,
                    "x_size": None,
                    "y_size": None,
                    "z_size": None,
                    "tlc_count": None,
                    "animation_count": None,
                    "data_length": None,
                },
                "animations": None,
            },
        }


#### Cube Files ################################################################
class CubeFile(BaseAssembler):  # noqa
    def __init__(self) -> None:
        super().__init__(serializer.cube_file_cube_file)


class CubeFileV1(CubeFile):
    def __init__(self, library: Library) -> None:
        super().__init__()
        self.populate(library)

    def populate(self, library: Library) -> None:
        data = CubeFileV1.template()
        data["file"] = library.populated_data

        self._populated_data = data

    def __len__(self) -> int:
        try:
            return (
                serializer.primary_header_primary_header.sizeof() * 2
                + len(self._populated_data["file"]["sha256"])
                + serializer.library_v1_secondary_header.sizeof()
                + self._populated_data["file"]["library"]["secondary_header"][
                    "data_length"
                ]
            )
        except (SizeofError, KeyError):
            raise ValueError("Data was not populated!")

    @staticmethod
    def template() -> Dict[str, Any]:
        return {
            "primary_header": {"type": "file", "version": 1},
            "file": None,
        }
