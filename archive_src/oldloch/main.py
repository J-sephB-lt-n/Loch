"""CLI entrypoint to the loch package"""

import argparse
import json
import shutil
from pathlib import Path

from loch import constants
from loch.cli import get_user_input_from_fixed_options
from loch.filesystem import filter_filepaths
from loch.databases import create_search_databases
from loch.search import run_search


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
        type=Path,
    )
    init_parser.add_argument(
        "--exclude_folders",
        help="These folders (and their subfolders) will not be included",
        nargs="*",
        metavar="DIR",
        type=Path,
    )
    init_parser.add_argument(
        "--include_filetypes",
        help="Only these file extensions will be included e.g. --include_filetypes .yaml .ini .json",
        nargs="*",
        metavar="EXT",
        type=Path,
    )
    init_parser.add_argument(
        "--exclude_filetypes",
        help="Files with these extensions will be excluded e.g. --exclude_filetypes .yaml .ini .json",
        nargs="*",
        metavar="EXT",
        type=Path,
    )

    args = arg_parser.parse_args()

    if args.command == "init":
        if constants.LOCAL_PROJECT_PATH.exists():
            print(
                f"Existing `loch` project found in directory '{constants.LOCAL_PROJECT_PATH}'"
            )
            print("Run `loch clean` to delete the existing project")
            exit()

        filepaths_to_process: list[Path] = filter_filepaths(
            filepaths=Path(".").rglob("*"),
            include_folders=args.include_folders,
            exclude_folders=args.exclude_folders,
            include_filetypes=args.include_filetypes,
            exclude_filetypes=args.exclude_filetypes,
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
            "Automatic tagging (using a LLM)",
        ):
            while True:
                user_input: str = input(f"Do you wish to include {search_name}? [y/n] ")
                if user_input in ("y", "n"):
                    break
                print("\t invalid input - accepted values are ['y', 'n']")
            search_methods[search_name] = user_input == "y"

        if (
            search_methods["semantic vector search"]
            and search_methods["keyword search (bm25)"]
        ):
            search_methods["hybrid search (semantic + bm25)"] = True
        else:
            search_methods["hybrid search (semantic + bm25)"] = False

        query_rewrite_methods: dict[str, bool] = {}
        for rewrite_method in ("Hypothetical Document Embeddings (HyDE)",):
            while True:
                user_input: str = input(
                    f"Do you want to include query rewriting method '{rewrite_method}'? [y/n] "
                )
                if user_input in ("y", "n"):
                    break
                print("\t invalid input - accepted values are ['y', 'n']")
            query_rewrite_methods[rewrite_method] = user_input == "y"

        with open(constants.LOCAL_PROJECT_PATH / "config.json", "w") as file:
            json.dump(
                {
                    "available_search_methods": search_methods,
                    "available_query_rewrite_methods": query_rewrite_methods,
                },
                file,
                indent=4,
            )

        create_search_databases(filepaths_to_process)

    elif args.command == "search":
        run_search()

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
