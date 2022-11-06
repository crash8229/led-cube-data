#!/usr/bin/env python3

from yaml import safe_load as load
from pathlib import Path
from typing import Dict, Set, Union, Tuple, Iterable, Optional, List
from string import Template
import subprocess


# Construct templates
STRUCT_STR = Template("construct.Struct(${fields})")
BITSTRUCT_STR = Template("construct.BitStruct(${fields})")
ARRAY_STR = Template("construct.Array(${size}, ${element})")
BITWISE_STR = Template("construct.Bitwise(${item})")
SWITCH_STR = Template("construct.Switch(${switch}, ${cases})")


class Types:
    __types: Dict[str, Tuple[Template, bool]] = {
        "u": (Template("construct.BytesInteger(${num})"), False),
        "b": (Template("construct.BitsInteger(${num})"), True),
        "str": (Template("construct.PaddedString(${size}, 'utf8')"), False),
    }

    def __init__(self) -> None:
        self.__custom_types: Dict[str, str] = dict()
        self.__import_stack: List[str] = list()

    @property
    def custom_types(self) -> Dict[str, str]:
        return self.__custom_types.copy()

    def clear_imports(self) -> None:
        self.__import_stack.clear()

    def get_type(
        self,
        type_str: Union[str, dict],
        meta_id: str,
        seq_ids: Iterable[str],
        size: int = 0,
    ) -> Tuple[str, bool]:
        if isinstance(type_str, dict):
            if "switch-on" in type_str:
                cases = self._process_switch_cases(type_str["cases"], seq_ids, meta_id)
                return (
                    SWITCH_STR.substitute(
                        switch=self._process_expr_str(type_str["switch-on"], seq_ids),
                        cases=cases[0],
                    ),
                    cases[1],
                )

        elif isinstance(type_str, str):

            # Is the type from the imports
            if type_str in self.__import_stack:
                return f"{type_str}_{type_str}", False

            # Is the type in the current ksy scope
            if f"{meta_id}_{type_str}" in self.__custom_types:
                return f"{meta_id}_{type_str}", False

            # Is the type a base type
            if type_str in self.__types:
                if type_str == "str":
                    return (
                        self.__types[type_str][0].substitute(size=size),
                        self.__types[type_str][1],
                    )
            elif type_str[0] in self.__types:
                key = type_str[0]
                num = type_str[1:]
                return self.__types[key][0].substitute(num=num), self.__types[key][1]

        raise TypeError(f"Unknown type entry: {type_str}")

    def add_custom_type(self, name: str, definition: str) -> None:
        self.__custom_types[name] = definition

    def add_custom_types(self, types: Dict[str, str]) -> None:
        self.__custom_types.update(types)

    def build_types(self, data: dict, meta_id: str) -> None:
        for type_key in data.keys():
            # Process seq tag
            struct_fields = Serializer.process_seq(data[type_key]["seq"], self, meta_id)

            struct_type = BITSTRUCT_STR if struct_fields[1] else STRUCT_STR
            struct_entry = struct_type.substitute(fields=struct_fields[0][:-2])

            self.__custom_types[f"{meta_id}_{type_key}"] = struct_entry

    def build_imports(self, base_dir: Path, import_files: Iterable[str]) -> None:
        import_list = list()
        for import_file in import_files:
            ksy_file = base_dir.joinpath(f"{import_file}.ksy")
            ksy_id = ksy_file.stem
            import_list.append(ksy_id)
            if f"{ksy_id}_{ksy_id}" in self.__custom_types:
                continue
            seq_name, seq_type, types = Serializer.process_ksy(ksy_file, self)
            types.add_custom_type(f"{seq_name}_{seq_name}", seq_type)
        self.__import_stack = import_list

    # TODO: Support enums types
    def build_enums(self, data: dict):
        pass

    def _process_switch_cases(
        self, cases: dict, seq_ids: Iterable[str], meta_id: str
    ) -> Tuple[str, bool]:
        case_str = Template("${key}: ${value}, ")
        result = "{"
        bit_type = False
        for key, value in cases.items():
            val = self.get_type(value, meta_id, seq_ids)
            bit_type |= val[1]
            result += case_str.substitute(key=key, value=val[0])
        return result[:-2] + "}", bit_type

    @staticmethod
    def _process_expr_str(expr_str: str, seq_ids: Iterable[str]) -> str:
        for seq_id in seq_ids:
            if seq_id in expr_str:
                idx = expr_str.index(seq_id)
                expr_str = (
                    f"{expr_str[:idx-1 if idx else idx]}construct.this.{expr_str[idx:]}"
                )
        return expr_str.replace("/", "//")

    @staticmethod
    def check_array(
        field: dict, seq_ids: Iterable[str]
    ) -> Tuple[bool, Union[int, str]]:
        array = False
        array_size: Union[int, str] = 0
        if "repeat" in field:
            array = True
            if "expr" in field["repeat"]:
                array_size = Types._get_array_size(field["repeat-expr"], seq_ids)
        return array, array_size

    @staticmethod
    def _get_array_size(repeat: str, ids: Iterable[str]) -> Union[str, int]:
        if isinstance(repeat, str):
            return Types._process_expr_str(repeat, ids)
        else:
            return repeat


class Serializer:
    @staticmethod
    def construct_serializers(ksy_files: Iterable[Path], out_file: Path) -> Path:
        # Assemble serializers
        serializers = Types()
        for yaml_file in ksy_files:
            seq_name, seq_type, seq_imports = Serializer.process_ksy(
                yaml_file, serializers
            )
            serializers.add_custom_type(f"{seq_name}_{seq_name}", seq_type)

        # Write the serializer module
        out_path = out_file
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as out:
            out.write("import construct\n\n")
            for seq_name, seq_type in serializers.custom_types.items():
                out.write(f"{seq_name} = {seq_type}\n\n")

        return out_path

    @staticmethod
    def process_ksy(
        ksy_file: Path, custom_types: Optional[Types] = None
    ) -> Tuple[str, str, Types]:
        ksy_dir = ksy_file.parent
        with open(ksy_file, "r") as f:
            yaml_data = load(f)

        # Get types and any custom types
        types = Types() if custom_types is None else custom_types
        if "imports" in yaml_data["meta"]:
            types.build_imports(ksy_dir, yaml_data["meta"]["imports"])
        else:
            types.build_imports(ksy_dir, [])
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
    def process_seq(seq: dict, types: Types, meta_id: str) -> Tuple[str, bool]:
        struct_fields = str()
        seq_ids: Set[str] = set()
        bit_type = False
        for field in seq:
            field_type = types.get_type(
                field["type"], meta_id, seq_ids, field["size"] if "size" in field else 0
            )
            bit_type |= field_type[1]
            struct_field = field_type[0]

            # Check if it is an array
            array, array_size = Types.check_array(field, seq_ids)

            if array:
                struct_field = f"{struct_field}"
                struct_fields += f"\"{field['id']}\" / {ARRAY_STR.substitute(size=array_size, element=struct_field)}, "
            else:
                struct_field = f"\"{field['id']}\" / {struct_field}"
                struct_fields += f"{struct_field}, "

            seq_ids.add(field["id"])
        return struct_fields, bit_type


if __name__ == "__main__":
    new_module = Serializer.construct_serializers(
        (
            # Path("./doc/file_specification/objects/frame.ksy"),
            # Path("./doc/file_specification/objects/animation.ksy"),
            # Path("./doc/file_specification/objects/library.ksy"),
            Path("./doc/file_specification/objects/cube_file.ksy"),
        ),
        Path("led_cube_data").joinpath("serializer.py"),
    )

    # Run Black formatter on new module
    subprocess.run(["black", "-q", f"{new_module}"])
