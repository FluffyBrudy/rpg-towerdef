import re
from pathlib import Path
from typing import Union


# file associated utils
def match_num(string: str) -> Union[float, int]:
    test = re.match(r"(\d+)", string)
    if not test:
        return float("inf")
    num_prefix = int(test.group(0))
    return num_prefix


# related to files
def convert_to_str_path(path: Union[str, Path]) -> str:
    if isinstance(path, Path):
        return str(path)
    return path


def get_dir(path: Union[str, Path]) -> str:
    is_posix_path = isinstance(path, Path)
    posix_path = path if is_posix_path else Path(path)

    if posix_path.is_dir():
        return str(path)
    return str(posix_path.parent)


def list_files_sorted(path: Union[str, Path], filter="*"):
    files = [str(file) for file in Path(get_dir(path)).glob(filter)]
    sorted_files = sorted(files, key=lambda file: match_num(file))
    return sorted_files
