"""
Search over a Knowledge Graph constructed by a generative language model
"""

from pathlib import Path
from typing import Literal, Optional

import networkx as nx

from loch import tui
from loch.data_models.query_algorithm import QueryAlgorithm
from loch.data_processing import text_chunking


class LlmKnowledgeGraph(QueryAlgorithm):
    """
    Search over a Knowledge Graph constructed by a generative language model
    
    Notes:
        - This implementation takes some inspiration from Zep, which itself took inspiration \
from Microsoft GraphRAG.
    """

    def setup(
        self,
        step: Literal["index", "query"],
        filepaths: Optional[list[Path]] = None,
    ) -> None:
        """
        Prepare (initialise) the algorithm for use

        Args:
            step:       step="index" processes all files for efficient future querying.
                        step="query" prepares the algorithm to process a user query.
            filepaths:  TODO
        """
        if step == "index":
            chunking_method: str = tui.launch_single_select(
                options=[x.value for x in text_chunking.TextChunkMethod],
                unselectable=[
                    x.value
                    for x in text_chunking.TextChunkMethod
                    if x.value not in ("Full doc (no chunking)")
                ],
            )
            chunker = text_chunking.CHUNKER_LOOKUP[
                text_chunking.TextChunkMethod(chunking_method)
            ]
            # graph = nx.Graph() # https://networkx.org/documentation/stable/tutorial.html

    def query(self, user_query: str):
        """
        Retrieve results most relevant to `user_query`
        """
        raise NotImplementedError

    def launch_query_interface(self) -> None:
        """
        Runs an interactive interface which gets a query from the user and processes it
        """
        print("llm_knowledge_graph is not yet implemented")
