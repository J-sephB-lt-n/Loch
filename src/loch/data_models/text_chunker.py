from typing import Protocol

from loch.data_processing.text_chunking.data_models import TextChunk


class TextChunker(Protocol):
    def __call__(
        self, source_doc_name: str, input_text: str
    ) -> tuple[TextChunk, ...]: ...
