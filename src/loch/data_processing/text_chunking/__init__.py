from enum import Enum


class AvailableChunkingMethods(str, Enum):
    FULL_DOC = "Full doc (no chunking)"
    FIXED_SIZE = "Fixed size chunks"
    SEMANTIC = "Semantic chunking"
    SPLIT_BY_REGEX = "Split by regex pattern"


from .fixed_size import fixed_size
from .semantic import semantic
from .split_by_regex import split_by_regex
