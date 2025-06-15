"""
Search over a Knowledge Graph constructed by a generative language model
"""

import importlib
from pathlib import Path
from typing import Literal, Optional

import networkx as nx

from loch import constants, tui
from loch.data_models.query_algorithm import QueryAlgorithm
from loch.data_processing import text_chunking
from loch.data_processing.text_chunking import TextChunk


class LlmKnowledgeGraph(QueryAlgorithm):
    """
    Search over a Knowledge Graph constructed by a generative language model
    
    Notes:
        - This implementation takes some inspiration from Zep, which itself took inspiration \
from Microsoft GraphRAG.
    """

    def __init__(self):
        self._local_alg_dir: Path = (
            constants.LOCAL_ALG_CONFIGS_PATH / self.__class__.__name__
        )
        self._local_alg_dir.mkdir()

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
            if filepaths is None:
                raise ValueError("filepaths must be provided when step='index'")

            with open(
                self._local_alg_dir / "explore_knowledge_graph.html", "w"
            ) as file:
                file.write(
                    importlib.resources.read_text(
                        "loch.algs.assets", "explore_knowledge_graph.html"
                    )
                )

            text_chunking_method: str = tui.launch_single_select(
                options=[x.value for x in text_chunking.TextChunkMethod],
                unselectable=[
                    x.value
                    for x in text_chunking.TextChunkMethod
                    if x.value not in ("Full doc (no chunking)")
                ],
            )
            text_chunker = text_chunking.CHUNKER_LOOKUP[
                text_chunking.TextChunkMethod(text_chunking_method)
            ]
            graph: nx.Graph = nx.Graph()
            for filepath in filepaths:
                graph.add_node(
                    f"source_doc={filepath}",  # node ID
                    name=str(filepath),
                    node_type="source_document",
                )
                with open(filepath, "r", encoding="utf-8") as file:
                    file_content: str = file.read()
                text_chunks: tuple[TextChunk, ...] = text_chunker(
                    source_doc_name=str(filepath), input_text=file_content
                )
                for chunk in text_chunks:
                    graph.add_node(
                        f"chunk={chunk.chunk_num_in_doc} doc={filepath}",
                        name=f"filepath.name chunk {chunk.chunk_num_in_doc}",
                        node_type="text_chunk",
                    )
            with open(
                self._local_alg_dir / "knowledge_graph_data.json",
                "w",
            ) as file:
                file.write(
                    nx.readwrite.json_graph.node_link_data(graph),
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
        print("llm_knowledge_graph is not yet implemented")
