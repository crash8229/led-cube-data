# led-cube-data
File specification used in my LED cube projects.
Currently, this package only includes parsers, serializers, and assemblers for Python.

The file specification is defined in ksy files and an ods spreadsheet. Both can be found [here](doc/file_specification).
Under the objects folder are more ksy files and test binaries.

Parsers for other languages can be made easily via the [Kaitai Struct compiler](https://kaitai.io/).
Only [parser.ksy](doc/file_specification/parser.ksy) needs to be compiled.
It references the other ksy files located under the objects folder and will be compiled as well.
