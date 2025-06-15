"""
Functions and utilities related to HTTP
"""

import socket


def find_free_port() -> int:
    """
    Find a free port by letting the OS assign one to us

    Notes:
        - The returned port is free at the time of assignment, but may \
not necessarily be free after this function ends (another process may \
pip you to it)
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("", 0))
        return sock.getsockname()[1]
