import json
from pathlib import Path

import lancedb
import lancedb.embeddings
import lancedb.pydantic

from loch import constants
from loch.cli import print_progress_bar


def create_search_databases(filepaths_to_process: list[Path]) -> None:
    """
    TODO
    """
    with open(constants.LOCAL_PROJECT_PATH / "config.json", "r") as file:
        config: dict = json.load(file)

    include_semantic: bool = config["available_search_methods"][
        "semantic vector search"
    ]
    include_bm25: bool = config["available_search_methods"]["keyword search (bm25)"]

    files_contents: dict[Path, str] = {}
    print("Reading in file contents")
    print_progress_bar(0, len(filepaths_to_process), bar_len=50)
    for file_num, filepath in enumerate(filepaths_to_process, start=1):
        with open(filepath, "r") as file:
            files_contents[filepath] = file.read()
            print_progress_bar(file_num, len(filepaths_to_process), bar_len=50)

    if include_semantic or include_bm25:
        vector_db = lancedb.connect(constants.VECTOR_DB_PATH)

        if include_semantic:
            print("loading embedding model")
            embed_model = (
                lancedb.embeddings.get_registry()
                .get("sentence-transformers")
                .create(
                    name="mixedbread-ai/mxbai-embed-large-v1",
                    device="cpu",
                )
            )
        if include_semantic and include_bm25:

            class Embedding(lancedb.pydantic.LanceModel):
                text: str = embed_model.SourceField()
                vector: lancedb.pydantic.Vector(embed_model.ndims()) = (
                    embed_model.VectorField()
                )
        elif include_semantic and not include_bm25:

            class Embedding(lancedb.pydantic.LanceModel):
                vector: lancedb.pydantic.Vector(embed_model.ndims()) = (
                    embed_model.VectorField()
                )
        elif not include_semantic and include_bm25:

            class Embedding(lancedb.pydantic.LanceModel):
                text: str = embed_model.SourceField()
        else:
            raise ValueError("Embedding schema not defined")

        vector_db_table = vector_db.create_table("vector_embeddings", schema=Embedding)
