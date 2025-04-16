"""
Definition of `BiMap` class
"""

from typing import Any


class BiMap:
    """
    A key-value store in which O(1) lookups can be performed in either
    direction (i.e. value lookup from key, or key lookup from value)
    """

    def __init__(self, pairs: list[tuple[Any, Any]]) -> None:
        self._value_lookup = {k: v for k, v in pairs}
        self._key_lookup = {v: k for k, v in pairs}

    def findkey(self, value):
        """
        Look up a key using a value
        """
        return self._key_lookup[value]

    def findval(self, key):
        """
        Look up a value using a key
        """
        return self._value_lookup[key]

    @property
    def keys(self) -> list:
        return list(self._value_lookup.keys())

    @property
    def values(self) -> list:
        return list(self._value_lookup.values())
