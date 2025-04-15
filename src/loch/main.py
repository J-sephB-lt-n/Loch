"""
Main app CLI entry script
"""

import argparse

import loch.core


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "command",
        help="Command to run",
    )
    args = arg_parser.parse_args()

    if args.command not in ("init", "query", "cleanup"):
        raise ValueError(
            f"Unknown command 'loch {args.command}'."
            "Valid options are 'loch init', 'loch query', 'loch cleanup'"
        )

    if args.command == "init":
        loch.core.loch_init()
    elif args.command == "query":
        loch.core.loch_query()
    elif args.command == "cleanup":
        loch.core.loch_cleanup()
