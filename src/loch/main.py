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

    if args.command == "init":
        loch.core.loch_init()
    elif args.command == "explore":
        loch.core.loch_explore()
    elif args.command == "query":
        loch.core.loch_query()
    elif args.command == "cleanup":
        loch.core.loch_cleanup()
    else:
        raise ValueError(
            f"Unknown command 'loch {args.command}'."
            "Valid options are "
            "['loch init', 'loch explore', 'loch query', 'loch cleanup']"
        )
