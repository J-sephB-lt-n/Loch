"""
Functions for interacting with the local filesystem
"""

from pathlib import Path
from typing import Optional


def is_in_dot_folder(path: Path) -> bool:
    """Returns True if the path is inside a dot-folder at any level."""
    return any(part.startswith(".") for part in path.parts)


def is_in_leading_underscore_folder(path: Path) -> bool:
    """Returns True if the path is inside a folder whose name has a leading underscore, at any level."""
    return any(part.startswith("_") for part in path.parts)


def list_filepaths(
    include_folders: Optional[list[str]] = None,
    exclude_folders: Optional[list[str]] = None,
    include_filetypes: Optional[list[str]] = None,
    exclude_filetypes: Optional[list[str]] = None,
    exclude_dot_folders: bool = True,
    exclude_leading_underscore_folders: bool = True,
) -> list[Path]:
    """
    TODO
    """
    filepaths_to_include: list[Path] = []
    for path in Path(".").rglob("*"):
        if not path.is_file():
            continue
        if include_filetypes and path.suffix not in include_filetypes:
            continue
        if exclude_dot_folders and is_in_dot_folder(path):
            continue
        if exclude_leading_underscore_folders and is_in_leading_underscore_folder(path):
            continue
        filepaths_to_include.append(path)

    return filepaths_to_include
