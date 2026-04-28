#!/usr/bin/env python3
"""Creates Python serializer modules from a KSY file."""

import subprocess
from collections.abc import Iterable
from pathlib import Path
from string import Template

from yaml import safe_load as load

# Construct templates
STRUCT_STR = Template("construct.Struct(${fields})")
BITSTRUCT_STR = Template("construct.BitStruct(${fields})")
ARRAY_STR = Template("construct.Array(${size}, ${element})")
BITWISE_STR = Template("construct.Bitwise(${item})")
SWITCH_STR = Template("construct.Switch(${switch}, ${cases})")


class Types:
    """Holds the list of types while parsing a KSY file and generates the code for a requested type."""

    def __init__(self) -> None:
        """."""
        self.__types: dict[str, tuple[Template, bool]] = {
            "u": (Template("construct.BytesInteger(${num})"), False),
            "b": (Template("construct.BitsInteger(${num})"), True),
            "str": (Template("construct.PaddedString(${size}, 'utf8')"), False),
            "None": (Template("construct.Bytes(${size})"), False),
        }
        self.__custom_types: dict[str, str] = {}
        self.__import_stack: list[str] = []
        self.__enum_types: dict[str, Template] = {}

    @property
    def custom_types(self) -> dict[str, str]:
        """Returns a copy of the custom type dictionary."""
        return self.__custom_types.copy()

    def clear_imports(self) -> None:
        """Clears the import stack list."""
        self.__import_stack.clear()

    def __get_type_from_string(
        self,
        field: dict,
        meta_id: str,
    ) -> tuple[str, bool] | None:
        type_str: str = field.get("type", "")
        size: int = field.get("size", 0)
        return_values: tuple[str, bool] | None = None

        # Is the type from the imports
        if type_str in self.__import_stack:
            return_values = (f"{type_str}_{type_str}", False)

        # Is the type in the current ksy scope
        elif f"{meta_id}_{type_str}" in self.__custom_types:
            return_values = (f"{meta_id}_{type_str}", False)

        # Is the type a base type
        elif type_str in self.__types and type_str == "str":
            return_values = (
                self.__types[type_str][0].substitute(size=size),
                self.__types[type_str][1],
            )
        elif type_str[0] in self.__types:
            key = type_str[0]
            num = type_str[1:]
            return_values = (
                self.__types[key][0].substitute(num=num),
                self.__types[key][1],
            )

        if "enum" in field and return_values is not None:
            if f"{meta_id}_{field['enum']}" in self.__enum_types:
                enum_type = self.__enum_types[f"{meta_id}_{field['enum']}"]
            else:
                msg = f"Enum {field['enum']} not defined"
                raise TypeError(msg)
            return_values = (
                enum_type.substitute(type=return_values[0]),
                return_values[1],
            )

        return return_values

    def get_type(
        self,
        field: dict,
        meta_id: str,
        seq_ids: Iterable[str],
    ) -> tuple[str, bool]:
        """Get the code string for a known type."""
        type_str: dict | str | None = field.get("type")
        size: int = field.get("size", 0)
        return_values: tuple[str, bool] | None = None

        if isinstance(type_str, dict) and "switch-on" in type_str:
            cases = self._process_switch_cases(type_str["cases"], seq_ids, meta_id)
            return_values = (
                SWITCH_STR.substitute(
                    switch=self._process_expr_str(type_str["switch-on"], seq_ids),
                    cases=cases[0],
                ),
                cases[1],
            )

        elif isinstance(type_str, str):
            return_values = self.__get_type_from_string(field=field, meta_id=meta_id)

        elif type_str is None:
            return_values = (
                self.__types["None"][0].substitute(size=size),
                self.__types["None"][1],
            )

        if not return_values:
            msg = f"Unknown type entry: {type_str}"
            raise TypeError(msg)

        return return_values

    def add_custom_type(self, name: str, definition: str) -> None:
        """Add a single custom type."""
        self.__custom_types[name] = definition

    def add_custom_types(self, types: dict[str, str]) -> None:
        """Add a dictionary containing one or more custom types."""
        self.__custom_types.update(types)

    def build_types(self, data: dict, meta_id: str) -> None:
        """Build types from a KSY sequence."""
        for type_key in data:
            # Process seq tag
            struct_fields = Serializer.process_seq(data[type_key]["seq"], self, meta_id)

            struct_type = BITSTRUCT_STR if struct_fields[1] else STRUCT_STR
            struct_entry = struct_type.substitute(fields=struct_fields[0][:-2])

            self.__custom_types[f"{meta_id}_{type_key}"] = struct_entry

    def build_imports(self, base_dir: Path, import_files: Iterable[str]) -> None:
        """Create custom types from the import list in a KSY file."""
        import_list = []
        for import_file in import_files:
            ksy_file = base_dir.joinpath(f"{import_file}.ksy")
            ksy_id = ksy_file.stem
            import_list.append(ksy_id)
            if f"{ksy_id}_{ksy_id}" in self.__custom_types:
                continue
            seq_name, seq_type, types = Serializer.process_ksy(ksy_file, self)
            types.add_custom_type(f"{seq_name}_{seq_name}", seq_type)
        self.__import_stack = import_list

    def build_enums(self, data: dict[str, dict[int, str]], meta_id: str) -> None:
        """Build an enum type(s)."""
        for type_name, type_values in data.items():
            enum_values = ", ".join((f"{v}={k}" for k, v in type_values.items()))
            self.__enum_types[f"{meta_id}_{type_name}"] = Template(
                f"construct.Enum(${{type}}, {enum_values})"
            )

    def _process_switch_cases(
        self, cases: dict, seq_ids: Iterable[str], meta_id: str
    ) -> tuple[str, bool]:
        case_str = Template("${key}: ${value}, ")
        result = "{"
        bit_type = False
        for key, value in cases.items():
            val = self.get_type({"type": value}, meta_id, seq_ids)
            bit_type |= val[1]
            result += case_str.substitute(key=key, value=val[0])
        return result[:-2] + "}", bit_type

    @staticmethod
    def _process_expr_str(expr_str: str, seq_ids: Iterable[str]) -> str:
        for seq_id in seq_ids:
            if seq_id in expr_str:
                idx = expr_str.index(seq_id)
                expr_str = f"{expr_str[: idx - 1 if idx else idx]}construct.this.{expr_str[idx:]}"
        return expr_str.replace("/", "//")

    @staticmethod
    def check_array(field: dict, seq_ids: Iterable[str]) -> tuple[bool, int | str]:
        """Checks if the given field string is an array and returns the size if it is."""
        array = False
        array_size: int | str = 0
        if "repeat" in field:
            array = True
            if "expr" in field["repeat"]:
                array_size = Types._get_array_size(field["repeat-expr"], seq_ids)
        return array, array_size

    @staticmethod
    def _get_array_size(repeat: str, ids: Iterable[str]) -> str | int:
        if isinstance(repeat, str):
            return Types._process_expr_str(repeat, ids)
        return repeat


class Serializer:
    """Builds Python serializer module from KSY files."""

    @staticmethod
    def construct_serializers(ksy_files: Iterable[Path], out_file: Path) -> Path:
        """Generate a serializer module from the given KSY file."""
        # Assemble serializers
        serializers = Types()
        for yaml_file in ksy_files:
            seq_name, seq_type, _ = Serializer.process_ksy(yaml_file, serializers)
            serializers.add_custom_type(f"{seq_name}_{seq_name}", seq_type)

        # Write the serializer module
        out_path = out_file
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w") as out:
            out.write("import construct\n\n")
            for seq_name, seq_type in serializers.custom_types.items():
                out.write(f"{seq_name} = {seq_type}\n\n")

        return out_path

    @staticmethod
    def process_ksy(
        ksy_file: Path, custom_types: Types | None = None
    ) -> tuple[str, str, Types]:
        """Build all the types and sequences from the given KSY file."""
        ksy_dir = ksy_file.parent
        with ksy_file.open("r") as f:
            yaml_data = load(f)

        # Get types and any custom types
        types = Types() if custom_types is None else custom_types
        if "imports" in yaml_data["meta"]:
            types.build_imports(ksy_dir, yaml_data["meta"]["imports"])
        else:
            types.build_imports(ksy_dir, [])
        if "enums" in yaml_data:
            types.build_enums(yaml_data["enums"], yaml_data["meta"]["id"])
        if "types" in yaml_data:
            types.build_types(yaml_data["types"], yaml_data["meta"]["id"])

        # Process seq tag
        struct_fields = Serializer.process_seq(
            yaml_data["seq"], types, yaml_data["meta"]["id"]
        )

        # Pop import list
        types.clear_imports()

        # Build the final struct
        struct_type = BITSTRUCT_STR if struct_fields[1] else STRUCT_STR
        return (
            yaml_data["meta"]["id"],
            struct_type.substitute(fields=struct_fields[0][:-2]),
            types,
        )

    @staticmethod
    def process_seq(seq: dict, types: Types, meta_id: str) -> tuple[str, bool]:
        """Process a sequence from a KSY file."""
        struct_fields = ""
        seq_ids: set[str] = set()
        bit_type = False
        for field in seq:
            field_type = types.get_type(field, meta_id, seq_ids)
            bit_type |= field_type[1]
            struct_field = field_type[0]

            # Check if it is an array
            array, array_size = Types.check_array(field, seq_ids)

            if array:
                struct_field = f"{struct_field}"
                struct_fields += f'"{field["id"]}" / {ARRAY_STR.substitute(size=array_size, element=struct_field)}, '
            else:
                struct_field = f'"{field["id"]}" / {struct_field}'
                struct_fields += f"{struct_field}, "

            seq_ids.add(field["id"])
        return struct_fields, bit_type


if __name__ == "__main__":
    new_module = Serializer.construct_serializers(
        (Path("./doc/file_specification/objects/cube_file.ksy"),),
        Path("led_cube_data").joinpath("serializer.py"),
    )

    # Run Black formatter on new module
    subprocess.run(["black", "-q", f"{new_module.resolve()}"], check=True)  # noqa: S603, S607
