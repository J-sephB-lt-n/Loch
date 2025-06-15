from loch.data_processing.text_chunking.data_models import TextChunk


def no_chunking(source_doc_name: str, input_text: str) -> tuple[TextChunk, ...]:
    return (
        TextChunk(
            source_doc_name=source_doc_name,
            start_idx=0,
            end_idx=len(input_text) - 1,
            text=input_text,
            chunk_num_in_doc=1,
        ),
    )
