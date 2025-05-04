"""
Implementation of Agentic Knowledge Distillation (Pyramid Search), as described in \
https://towardsdatascience.com/overcome-failing-document-ingestion-rag-strategies-with-agentic-knowledge-distillation/

The algorithm works by sequentially building increasingly higher level document abstractions/summaries\
, and then allowing a RAG model (retriever) to search over these generated abstractions.

The original algorithm is:
    1. Convert all documents into markdown
    2. LLM extracts atomic insights from a document one chunk at a time.
        - Insights are of the form subject-predicate-object (i.e. knowledge tuples) \
            e.g. (earth, rotates around, sun)
        - LLM must "write sentences as if English is the second language of the user
        - Original algorithm recommends processing using a moving window of 2 pages, so that each page \
            is seen twice by the LLM and it can correct it's own previous mistakes
    3. For each document, LLM distills the large list of atomic insights (knowledge tuples) into \
        higher-level concepts which connected related information within the whole document.
    4. For each document, the LLM distills the atomic insights and extracted concepts into a \
        document abstract.
    5. Additional information ("recollections") relevant across documents can be manually added \
        to the searchable (retrievable) data.
    6. The original post notes that chunks of the original raw documents might also be included,
        (i.e. vanilla RAG at the same time) but that the added token cost of including them was \
        not worth the marginal gain in information.
"""

from pathlib import Path
from typing import Literal, Optional

from loch.data_models.query_algorithm import QueryAlgorithm


class PyramidSearch(QueryAlgorithm):
    """
    This is my own implementation of Agentic Knowledge Distillation (pyramid search), as desribed in \
    https://towardsdatascience.com/overcome-failing-document-ingestion-rag-strategies-with-agentic-knowledge-distillation/
        
    Notes:
        - It differs from the original implementation in that I am processing whole documents at a time \
            (I will return to this at a later stage, if it is valuable)
    """

    def setup(
        self,
        step: Literal["index", "query"],
        filepaths: Optional[list[Path]] = None,
    ) -> None:
        """
        Prepare (initialise) the algorithm for use

        Args:
            step:   step="index" processes all files for efficient future querying.
                    step="query" prepares the algorithm to process a user query.
        """
        print("pyramid_search is not yet implemented")

    def query(self, user_query: str):
        """
        Retrieve results most relevant to `user_query`
        """
        raise NotImplementedError

    def launch_query_interface(self) -> None:
        """
        Runs an interactive interface which gets a query from the user and processes it
        """
        print("pyramid_search is not yet implemented")
