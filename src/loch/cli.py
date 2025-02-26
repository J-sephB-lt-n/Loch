"""CLI entrypoint to the loch package"""

import argparse
from pathlib import Path

from loch import constants
from loch.filesystem import list_filepaths
from loch.databases import vector_db


def main():
    arg_parser = argparse.ArgumentParser(
        description="Local search over files"
    )
    subparsers = arg_parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser(
        "init", 
        help="Create a new search database",
    )
    search_parser = subparsers.add_parser(
        "search", 
        help="Query local search database",
    )
    clean_parser = subparsers.add_parser(
        "clean", 
        help="Delete local search database",
    )

    init_parser.add_argument(
        "--dry_run",
        help="Show which files would be included, but do not actually run",
        action="store_true",
    )
    init_parser.add_argument(
        "--include_folders",
        help="Only these folders will be included",
        nargs="*",
        metavar="DIR",
    )
    init_parser.add_argument(
        "--exclude_folders",
        help="All folders aside from these folders will be included",
        nargs="*",
        metavar="DIR",
    )

    args = arg_parser.parse_args()

    if args.command == "init":
        if constants.LOCAL_PROJECT_PATH.exists():
            print(
                f"Existing `loch` project found in directory '{constants.LOCAL_PROJECT_PATH}'"
            )
            print("Run `loch clean` to delete the existing project")
            exit()
        filepaths_to_process: list[Path] = list_filepaths()
        if args.dry_run:
            for filepath in filepaths_to_process:
                print(filepath)

    elif args.command == "search":
        print("You ran the search command")

    elif args.command == "clean":
        print("You ran the clean command")
