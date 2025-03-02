"""CLI entrypoint to the loch package"""

import argparse
import json
import shutil
from pathlib import Path

from loch import constants
from loch.filesystem import list_filepaths
from loch.databases import create_search_databases


def main():
    arg_parser = argparse.ArgumentParser(description="Local search over files")
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
        help="Only these folders (and their subfolders) will be included",
        nargs="*",
        metavar="DIR",
    )
    (
        init_parser.add_argument(
            "--exclude_folders",
            help="All folders aside from these folders will be included",
            nargs="*",
            metavar="DIR",
        ),
    )
    init_parser.add_argument(
        "--include_filetypes",
        help="Only these file extensions will be included e.g. --include_filetypes .yaml .ini .json",
        nargs="*",
        metavar="EXT",
    )

    args = arg_parser.parse_args()

    if args.command == "init":
        if constants.LOCAL_PROJECT_PATH.exists():
            print(
                f"Existing `loch` project found in directory '{constants.LOCAL_PROJECT_PATH}'"
            )
            print("Run `loch clean` to delete the existing project")
            exit()

        filepaths_to_process: list[Path] = list_filepaths(
            include_filetypes=args.include_filetypes,
        )
        print(f"including {len(filepaths_to_process):,} files")
        if args.dry_run:
            print("The following files would be included:")
            for filepath in filepaths_to_process:
                print("\t", filepath)
            exit()

        constants.LOCAL_PROJECT_PATH.mkdir()
        constants.LOCAL_DATABASES_PATH.mkdir()

        search_methods: dict[str, bool] = {}
        for search_name in (
            "semantic vector search",
            "keyword search (bm25)",
        ):
            while True:
                user_input: str = input(f"Do you wish to include {search_name}? [y/n] ")
                if user_input in ("y", "n"):
                    break
                print("\t invalid input - accepted values are ['y', 'n']")
            search_methods[search_name] = user_input == "y"

        with open(constants.LOCAL_PROJECT_PATH / "config.json", "w") as file:
            json.dump(
                {
                    "available_search_methods": search_methods,
                },
                file,
                indent=4,
            )

        create_search_databases(filepaths_to_process)

    elif args.command == "search":
        print("You ran the search command")

    elif args.command == "clean":
        if not constants.LOCAL_PROJECT_PATH.exists():
            print(f"No local project found at '{constants.LOCAL_PROJECT_PATH}'")
            exit()
        user_confirmation = input(
            "Are you sure that you want to delete all databases and indexes?\
 (anything other than 'yes' will abort): "
        )
        if user_confirmation == "yes":
            shutil.rmtree(constants.LOCAL_PROJECT_PATH)
            print("deleted `loch` project")
        else:
            print("..aborted")
