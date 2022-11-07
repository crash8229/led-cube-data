# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

from led_cube_data.parser import primary_header
from led_cube_data.parser import animation_v1
class Animation(KaitaiStruct):
    """LED Cube animation."""
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.primary_header = primary_header.PrimaryHeader(self._io)
        _on = self.primary_header.version
        if _on == 1:
            self.animation = animation_v1.AnimationV1(self._io)
        self.sha256 = self._io.read_bytes(32)


