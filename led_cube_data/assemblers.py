from hashlib import sha256
from copy import deepcopy
from typing import Sequence, Dict, Any
from construct import SizeofError

from led_cube_data import serializer


#### Frames ####################################################################
class Frame:
    @property
    def populated_data(self) -> Dict[str, Any]:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError


class FrameV1(Frame):
    def __init__(self, duration: int, tlc_states: Sequence[Sequence[int]]) -> None:
        self.__populated_data: Dict[str, Any] = dict()
        self.populate(duration, tlc_states)

    @property
    def populated_data(self) -> Dict[str, Any]:
        return deepcopy(self.__populated_data)

    def populate(self, duration: int, tlc_states: Sequence[Sequence[int]]) -> None:
        data = self.template()
        data["frame"]["secondary_header"]["duration"] = duration
        data["frame"]["secondary_header"]["data_length"] = len(tlc_states) * 24
        data["frame"]["tlc_states"] = [{"state": s} for s in tlc_states]

        self.__populated_data = data

    def generate(self) -> bytes:
        try:
            return serializer.frame_frame.build(self.__populated_data)
        except KeyError:
            raise ValueError("Data was not populated!")

    def __len__(self) -> int:
        try:
            return (
                serializer.primary_header_primary_header.sizeof()
                + serializer.frame_v1_secondary_header.sizeof()
                + self.__populated_data["frame"]["secondary_header"]["data_length"]
            )
        except (SizeofError, KeyError):
            raise ValueError("Data was not populated!")

    @staticmethod
    def template() -> Dict[str, Any]:
        return {
            "primary_header": {"type": 0, "version": 1},
            "frame": {
                "secondary_header": {"duration": None, "data_length": None},
                "tlc_states": None,
            },
        }


#### Animations ################################################################
class Animation:
    @property
    def populated_data(self) -> Dict[str, Any]:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError


class AnimationV1(Animation):
    def __init__(
        self,
        name: str,
        timestamp: int,
        tlc_count: int,
        frame_count: int,
        frames: Sequence[Frame],
    ) -> None:
        self.__populated_data: Dict[str, Any] = dict()
        self.populate(name, timestamp, tlc_count, frame_count, frames)

    @property
    def populated_data(self) -> Dict[str, Any]:
        return deepcopy(self.__populated_data)

    def populate(
        self,
        name: str,
        timestamp: int,
        tlc_count: int,
        frame_count: int,
        frames: Sequence[Frame],
    ) -> None:
        data = AnimationV1.template()
        data["animation"]["secondary_header"]["name"] = name
        data["animation"]["secondary_header"]["time"] = timestamp
        data["animation"]["secondary_header"]["tlc_count"] = tlc_count
        data["animation"]["secondary_header"]["frame_count"] = frame_count

        # Calculate data length
        data_length = 4  # 4 bytes for CRC
        data_length += sum((len(fr) for fr in frames))
        data["animation"]["secondary_header"]["data_length"] = data_length

        # Create frame data
        data["animation"]["frames"] = [f.populated_data for f in frames]

        # Generate CRC
        data["sha256"] = sha256(
            serializer.animation_v1_animation_v1.build(data["animation"])
        ).digest()

        self.__populated_data = data

    def generate(self) -> bytes:
        try:
            return serializer.animation_animation.build(self.__populated_data)
        except KeyError:
            raise ValueError("Data was not populated!")

    def __len__(self) -> int:
        try:
            return (
                serializer.primary_header_primary_header.sizeof()
                + serializer.animation_v1_secondary_header.sizeof()
                + self.__populated_data["animation"]["secondary_header"]["data_length"]
            )
        except (SizeofError, KeyError):
            raise ValueError("Data was not populated!")

    @staticmethod
    def template() -> Dict[str, Any]:
        return {
            "primary_header": {"type": 1, "version": 1},
            "animation": {
                "secondary_header": {
                    "name": None,
                    "time": None,
                    "tlc_count": None,
                    "frame_count": None,
                    "data_length": None,
                },
                "frames": None,
            },
            "crc": None,
        }


#### Libraries #################################################################
class Library:
    @property
    def populated_data(self) -> Dict[str, Any]:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError


class LibraryV1(Library):
    def __init__(
        self,
        name: str,
        timestamp: int,
        animation_count: int,
        animations: Sequence[Animation],
    ) -> None:
        self.__populated_data: Dict[str, Any] = dict()
        self.populate(name, timestamp, animation_count, animations)

    @property
    def populated_data(self) -> Dict[str, Any]:
        return deepcopy(self.__populated_data)

    def populate(
        self,
        name: str,
        timestamp: int,
        animation_count: int,
        animations: Sequence[Animation],
    ) -> None:
        data = LibraryV1.template()
        data["library"]["secondary_header"]["name"] = name
        data["library"]["secondary_header"]["time"] = timestamp
        data["library"]["secondary_header"]["animation_count"] = animation_count

        # Calculate data length
        data_length = 4  # 4 bytes for CRC
        data_length += sum((len(ani) for ani in animations))
        data["library"]["secondary_header"]["data_length"] = data_length

        # Create frame data
        data["library"]["animations"] = [ani.populated_data for ani in animations]

        # Generate CRC
        data["sha256"] = sha256(
            serializer.library_v1_library_v1.build(
                data["library"]
            )
        ).digest()

        self.__populated_data = data

    def generate(self) -> bytes:
        try:
            return serializer.library_library.build(self.__populated_data)
        except KeyError:
            raise ValueError("Data was not populated!")

    def __len__(self) -> int:
        try:
            return (
                serializer.primary_header_primary_header.sizeof()
                + serializer.library_v1_secondary_header.sizeof()
                + self.__populated_data["library"]["secondary_header"]["data_length"]
            )
        except (SizeofError, KeyError):
            raise ValueError("Data was not populated!")

    @staticmethod
    def template() -> Dict[str, Any]:
        return {
            "primary_header": {"type": 2, "version": 1},
            "library": {
                "secondary_header": {
                    "name": None,
                    "time": None,
                    "animation_count": None,
                    "data_length": None,
                },
                "crc": None,
                "animations": None,
            },
        }


#### Cube Files ################################################################
class CubeFile:
    @property
    def populated_data(self) -> Dict[str, Any]:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError


class CubeFileV1(Library):
    def __init__(self, library: Library) -> None:
        self.__populated_data: Dict[str, Any] = dict()
        self.populate(library)

    @property
    def populated_data(self) -> Dict[str, Any]:
        return deepcopy(self.__populated_data)

    def populate(self, library: Library) -> None:
        data = CubeFileV1.template()
        data["file"] = library.populated_data

        self.__populated_data = data

    def generate(self) -> bytes:
        try:
            return serializer.cube_file_cube_file.build(self.__populated_data)
        except KeyError:
            raise ValueError("Data was not populated!")

    def __len__(self) -> int:
        try:
            return (
                serializer.primary_header_primary_header.sizeof() * 2
                + serializer.library_v1_secondary_header.sizeof()
                + self.__populated_data["file"]["secondary_header"]["data_length"]
            )
        except (SizeofError, KeyError):
            raise ValueError("Data was not populated!")

    @staticmethod
    def template() -> Dict[str, Any]:
        return {
            "primary_header": {"type": 3, "version": 1},
            "file": None,
        }
