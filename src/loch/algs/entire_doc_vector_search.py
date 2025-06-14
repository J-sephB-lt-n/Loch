"""
Definition of EntireDocumentVectorSearch algorithm, which embeds each document as a \
single vector and facilitates search over those vectors
"""

import json
import logging
from pathlib import Path
from typing import Final, Literal, Optional

import lancedb
import numpy as np
from lancedb.rerankers import RRFReranker

from loch import constants, tui
from loch.data_models.query_algorithm import QueryAlgorithm
from loch.data_processing import text_chunking
from loch.llm.embeddings.model2vec import model2vec_client
from loch.utils.logging_utils import get_logger

logger: logging.Logger = get_logger(__name__)


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
            if filepaths is None:
                raise ValueError("filepaths must be provided when step='index'")

            chunking_method: str = tui.launch_single_select(
                options=[x.value for x in text_chunking.TextChunkMethod],
                unselectable=[
                    x.value
                    for x in text_chunking.TextChunkMethod
                    if x.value not in ("Full doc (no chunking)")
                ],
            )
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
                        "filepath": filepath.as_posix(),
                        "vector": vector,
                        "text": text,
                    }
                    for filepath, vector, text in zip(
                        filepaths,
                        semantic_vectors.tolist(),
                        list(files_contents.values()),
                    )
                ],
            )
            self._db_table.create_fts_index(
                "text",
                use_tantivy=False,  # use native lancedb FTS
                tokenizer_name="en_stem",  # use stemming
            )

        elif step == "query":
            self._db_table = self._db.open_table(
                self._vector_table_name,
            )

    def query(
        self,
        search_query: str,
        search_method: Literal[
            "Semantic Search",
            "Full-Text Search (BM25)",
            "Hybrid Search (Semantic+BM25)",
        ],
        top_k: int,
    ) -> list[dict]:
        """
        Retrieve results most relevant to `search_query` using method `search_method`
        """
        search_query_embedding: Optional[np.ndarray] = None
        if search_method in ("Semantic Search", "Hybrid Search (Semantic+BM25)"):
            search_query_embedding = self._embed_model.encode(search_query)

        VECTOR_DIST_METRIC: Final[str] = "cosine"

        match search_method:
            case "Semantic Search":
                return (
                    self._db_table.search(search_query_embedding)
                    .distance_type(VECTOR_DIST_METRIC)
                    .limit(top_k)
                    .select(["filepath"])
                    .to_list()
                )
            case "Full-Text Search (BM25)":
                return (
                    self._db_table.search(search_query)
                    .limit(top_k)
                    .select(["filepath"])
                    .to_list()
                )
            case "Hybrid Search (Semantic+BM25)":
                return (
                    self._db_table.search(query_type="hybrid")
                    .vector(search_query_embedding)
                    .distance_type(
                        VECTOR_DIST_METRIC
                    )  # this applies to the vector search
                    .text(search_query)
                    .limit(50)  # this is the prefetch size
                    .rerank(
                        reranker=RRFReranker(K=60),
                    )
                    .select(["filepath"])
                    .to_list()
                )[:top_k]
            case _:
                raise ValueError(f"Search method '{search_method}' is not supported")

    def launch_query_interface(self) -> None:
        """
        Runs an interactive interface which gets a query from the user and processes it
        """
        search_method = tui.launch_single_select(
            options=[
                "Semantic Search",
                "Full-Text Search (BM25)",
                "Hybrid Search (Semantic+BM25)",
            ],
        )
        while True:
            user_query: str = input(
                "Please enter your search query " + "(submit 'exit' to quit): \n"
            ).strip()
            if user_query == "exit":
                logger.info(" ...exiting entire document vector search query interface")
                return
            results = self.query(
                search_query=user_query,
                search_method=search_method,
                top_k=8,
            )
            print(
                json.dumps(
                    results,
                    indent=4,
                )
            )

    def explore(self) -> None:
        """
        Provides an interactive exploration of the vector database.
        """
        print("explore() method not implemented")
