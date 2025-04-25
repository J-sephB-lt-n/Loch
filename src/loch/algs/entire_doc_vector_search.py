"""
Definition of EntireDocumentVectorSearch algorithm, which embeds each document as a \
single vector and facilitates search over those vectors
"""

from pathlib import Path
from typing import Literal, Optional

import lancedb
import numpy as np

from loch import constants
from loch.data_models.query_algorithm import QueryAlgorithm
from loch.llm.embeddings.model2vec import model2vec_client


class EntireDocumentVectorSearch(QueryAlgorithm):
    """
    Search by embedding the entire document (semantic and BM25)
    """

    def __init__(self) -> None:
        self._vector_table_name = "entire_doc_embeddings"

    def setup(
        self, step: Literal["index", "query"], filepaths: Optional[list[Path]] = None
    ) -> None:
        """
        Prepare (initialise) the algorithm for use

        Args:
            step:   step="index" processes all files for efficient future querying.
                    step="query" prepares the algorithm to process a user query.
        """
        self._db = lancedb.connect(constants.VECTOR_DB_PATH)
        model2vec_client.initialise_if_not_initialised()
        self._embed_model = model2vec_client.embed_model

        if step == "index":
            files_contents: dict[Path, str] = {}
            for filepath in filepaths:
                with open(filepath, "r") as file:
                    files_contents[filepath] = file.read()

            semantic_vectors: np.ndarray = self._embed_model.encode(
                list(files_contents.values()),
            )

            self._db_table = self._db.create_table(
                self._vector_table_name,
                data=[
                    {
                        "vector": vector,
                        "text": text,
                    }
                    for vector, text in zip(
                        semantic_vectors.tolist(),
                        list(files_contents.values()),
                    )
                ],
            )
            self._db_table.create_fts_index("text", use_tantivy=False)

        elif step == "query":
            self._db_table = self._db.open_table(
                self._vector_table_name,
            )

    def query(self, user_query: str):
        """
        Retrieve results most relevant to `user_query`
        """
        raise NotImplementedError

    def launch_query_interface(self) -> None:
        """
        Runs an interactive interface which gets a query from the user and processes it
        """
        print("fts_bm25 is not yet implemented")
