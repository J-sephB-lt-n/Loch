import pydantic


class TextChunk(pydantic.BaseModel):
    source_doc_name: str
    start_idx: int
    end_idx: int
    text: str
