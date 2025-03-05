import json
from pathlib import Path

import lancedb
import lancedb.pydantic

from loch import constants
from loch.cli import print_progress_bar
from loch.language_models.semantic_vector_embedding import (
    create_semantic_vector_embedding_model,
)


def create_search_databases(filepaths_to_process: list[Path]) -> None:
    """
    Add the contents of each included file into search databases
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
        print("Creating vector database")
        vector_db = lancedb.connect(constants.VECTOR_DB_PATH)

        if include_semantic:
            print("loading embedding model")
            embed_model = create_semantic_vector_embedding_model(
                model_name=constants.DEFAULT_SEMANTIC_EMBEDDING_MODEL_NAME,
            )

            class Embedding(lancedb.pydantic.LanceModel):
                filepath: str
                text: str = embed_model.SourceField()
                vector: lancedb.pydantic.Vector(embed_model.ndims()) = (
                    embed_model.VectorField()
                )
        elif not include_semantic:

            class Embedding(lancedb.pydantic.LanceModel):
                filepath: str
                text: str
        else:
            raise ValueError("Embedding schema not defined")

        print("Adding vectors to vector database")
        vector_db_table = vector_db.create_table("vector_search", schema=Embedding)
        vector_db_table.add(
            [
                {
                    "filepath": str(filepath),
                    "text": file_contents,
                }
                for filepath, file_contents in files_contents.items()
            ]
        )

        if include_bm25:
            print("Creating Full-Text-Search (FTS) index on vector database")
            vector_db_table.create_fts_index("text", use_tantivy=True)
