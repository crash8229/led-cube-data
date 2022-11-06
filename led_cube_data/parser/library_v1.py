# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

from led_cube_data.parser import animation
class LibraryV1(KaitaiStruct):
    """Version 1 of the library specification."""
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.secondary_header = LibraryV1.SecondaryHeader(self._io, self, self._root)
        self.crc = self._io.read_u4be()
        self.animations = [None] * (self.secondary_header.animation_count)
        for i in range(self.secondary_header.animation_count):
            self.animations[i] = animation.Animation(self._io)


    class SecondaryHeader(KaitaiStruct):
        """Houses the library metadata."""
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name = (self._io.read_bytes(32)).decode(u"UTF-8")
            self.time = self._io.read_u8be()
            self.animation_count = self._io.read_u4be()
            self.data_length = self._io.read_u8be()



