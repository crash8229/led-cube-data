# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

from led_cube_data.parser import primary_header
from led_cube_data.parser import library
from led_cube_data.parser import animation
from led_cube_data.parser import cube_file
from led_cube_data.parser import frame
class Parser(KaitaiStruct):
    """LED Cube Master Parser
    This parser looks at the primary header to determine how to parse the data
    provided. This parser is the recommended method to process data related to the
    LED Cube specification.
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.primary_header = primary_header.PrimaryHeader(self._io)

    @property
    def object(self):
        """This is where the data is actually parsed."""
        if hasattr(self, '_m_object'):
            return self._m_object

        _pos = self._io.pos()
        self._io.seek(0)
        _on = self.primary_header.type
        if _on == primary_header.PrimaryHeader.Type.frame:
            self._m_object = frame.Frame(self._io)
        elif _on == primary_header.PrimaryHeader.Type.animation:
            self._m_object = animation.Animation(self._io)
        elif _on == primary_header.PrimaryHeader.Type.library:
            self._m_object = library.Library(self._io)
        elif _on == primary_header.PrimaryHeader.Type.file:
            self._m_object = cube_file.CubeFile(self._io)
        self._io.seek(_pos)
        return getattr(self, '_m_object', None)


