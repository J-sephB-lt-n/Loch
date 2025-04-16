"""
Functions for interacting with the local filesystem
"""

from pathlib import Path
from typing import Iterable, Optional


def is_in_dot_folder(path: Path) -> bool:
    """Returns True if the path is inside a dot-folder at any level."""
    return any(part.startswith(".") for part in path.parts)


def is_in_leading_underscore_folder(path: Path) -> bool:
    """Returns True if the path is inside a folder whose name has a leading underscore, at any level."""
    return any(part.startswith("_") for part in path.parts)


def filter_filepaths(
    filepaths: Iterable[Path],
    include_folders: Optional[list[Path]] = None,
    exclude_folders: Optional[list[Path]] = None,
    include_filetypes: Optional[list[str]] = None,
    exclude_filetypes: Optional[list[str]] = None,
    exclude_dot_folders: bool = True,
    exclude_leading_underscore_folders: bool = True,
) -> list[Path]:
    """
    Return all `filepaths` which match all of \
    the given criteria

    Args:
        filepaths (Iterable[Path]): TODO e.g. 
        include_folders (list, optional): Only these folders (and their subfolders) will be included
        exclude_folders (list, optional): These folders (and their subfolders) will not be included
        include_filetypes (list, optional): Only files with these extensions will be included
        exclude_filetypes (list, optional): Files with these extensions will not be included
        exclude_dot_folders (bool, optional): If `True` (default), paths containing a dot folder (a \
                        directory name with a leading '.') will be excluded
                        Currently, this also excludes dotfiles (e.g. .env)
        exclude_leading_underscore_folders (bool, optional): If `True` (default), paths containing \
                        a directory with a leading '_' in it's name will be excluded
                        Currently, this also excludes leading-underscore files (e.g. _shared.ini)
    """
    filepaths_to_include: list[Path] = []
    for path in filepaths:  # Path(".").rglob("*"):
        if path.suffix is None:
            # print(f"{path} excluded for no file suffix")
            continue
        if include_folders:
            include = False
            for incl_dir in include_folders:
                if path.parts[: len(incl_dir.parts)] == incl_dir.parts:
                    include = True
                    break
            if not include:
                # print(f"{path} excluded for not in `include_folders`")
                continue
        if exclude_folders:
            exclude = False
            for excl_dir in exclude_folders:
                if path.parts[: len(excl_dir.parts)] == excl_dir.parts:
                    exclude = True
                    break
            if exclude:
                # print(f"{path} excluded for in `exclude_folders`")
                continue
        if include_filetypes and path.suffix not in include_filetypes:
            # print(f"{path} excluded for .suffix not in `include_filetypes`")
            continue
        if exclude_filetypes and path.suffix in exclude_filetypes:
            # print(f"{path} excluded for .suffix in `exclude_filetypes`")
            continue
        if exclude_dot_folders and is_in_dot_folder(path):
            # print(f"{path} excluded for is_in_dot_folder(path)")
            continue
        if exclude_leading_underscore_folders and is_in_leading_underscore_folder(path):
            # print(f"{path} excluded for is_in_leading_underscore_folder(path)")
            continue

        filepaths_to_include.append(path)

    return filepaths_to_include
