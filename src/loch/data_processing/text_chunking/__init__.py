from enum import Enum

from loch.data_models.text_chunker import TextChunker

from .data_models import TextChunk
from .fixed_size import fixed_size
from .no_chunking import no_chunking
from .semantic import semantic
from .split_by_regex import split_by_regex


class TextChunkMethod(str, Enum):
    FULL_DOC = "Full doc (no chunking)"
    FIXED_SIZE = "Fixed size chunks"
    SEMANTIC = "Semantic chunking"
    SPLIT_BY_REGEX = "Split by regex pattern"


CHUNKER_LOOKUP: dict[TextChunkMethod, TextChunker] = {
    TextChunkMethod.FULL_DOC: no_chunking,
    TextChunkMethod.FIXED_SIZE: fixed_size,
    TextChunkMethod.SEMANTIC: semantic,
    TextChunkMethod.SPLIT_BY_REGEX: split_by_regex,
}

assert sorted(CHUNKER_LOOKUP.keys()) == sorted([x.value for x in TextChunkMethod])
