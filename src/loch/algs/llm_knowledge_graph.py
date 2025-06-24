"""
Search over a Knowledge Graph constructed by a generative language model
"""

import functools
import http.server
import importlib
import json
import logging
import socketserver
import webbrowser
from pathlib import Path
from typing import Literal, Optional

import networkx as nx
from tqdm import tqdm

from loch import constants, tui
from loch.data_models.query_algorithm import QueryAlgorithm
from loch.data_processing import text_chunking
from loch.data_processing.text_chunking import TextChunk
from loch.llm.client import LlmClient
from loch.llm.tasks import extract_semantic_triples
from loch.tui import get_llm_config_from_user
from loch.utils.logging_utils import get_logger

logger: logging.Logger = get_logger(__name__)


class LlmKnowledgeGraph(QueryAlgorithm):
    """
    Search over a Knowledge Graph constructed by a generative language model
    
    Notes:
        - This implementation takes some inspiration from Zep, which itself took inspiration \
from Microsoft GraphRAG.
    """

    def __init__(self):
        self._local_alg_dir: Path = (
            constants.LOCAL_ALG_CONFIGS_PATH / "llm_knowledge_graph"
        )

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
        self.llm_config = get_llm_config_from_user()
        self._llm_client = LlmClient(
            base_url=self.llm_config["base_url"],
            api_key=self.llm_config["api_key"],
            model_name=self.llm_config["model_name"],
            temperature=self.llm_config["temperature"],
            logger=logger,
        )

        if step == "index":
            if filepaths is None:
                raise ValueError("filepaths must be provided when step='index'")

            # write explore_knowledge_graph.html into file in local project directory #
            with open(
                self._local_alg_dir / "explore_knowledge_graph.html", "w"
            ) as file:
                file.write(
                    importlib.resources.read_text(
                        "loch.algs.assets.llm_knowledge_graph",
                        "explore_knowledge_graph.html",
                    )
                )

            # let the user choose a text-chunking method #
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

            # build the knowledge graph #
            graph: nx.DiGraph = nx.DiGraph()
            for filepath in tqdm(filepaths):
                source_file_node_id: str = f"source_doc={filepath}"
                graph.add_node(
                    source_file_node_id,
                    name=str(filepath),
                    node_type="source_document",
                )
                with open(filepath, "r", encoding="utf-8") as file:
                    file_content: str = file.read()
                text_chunks: tuple[TextChunk, ...] = text_chunker(
                    source_doc_name=str(filepath), input_text=file_content
                )
                for chunk in text_chunks:
                    chunk_node_id: str = (
                        f"chunk={chunk.chunk_num_in_doc} doc={filepath}"
                    )
                    graph.add_node(
                        chunk_node_id,
                        name=f"{filepath.name} chunk {chunk.chunk_num_in_doc}",
                        node_type="text_chunk",
                        text=chunk.text,
                    )
                    graph.add_edge(
                        chunk_node_id,
                        source_file_node_id,
                        relationship="is text subset of",
                    )
                    semantic_tuples: list[list[str]] = extract_semantic_triples(
                        text=chunk.text,
                        llm=self._llm_client,
                    )
                    for subj, pred, obj in semantic_tuples:
                        for x in (subj, obj):
                            if x not in graph:
                                graph.add_node(
                                    x,
                                    name=x,
                                    node_type="entity",
                                )
                            graph.add_edge(
                                chunk_node_id,
                                x,
                                relationship="is entity in",
                            )
                        graph.add_edge(
                            subj,
                            obj,
                            relationship=pred,
                        )

            # save the knowledge graph in the local project directory #
            with open(
                self._local_alg_dir / "knowledge_graph_data.json",
                "w",
            ) as file:
                json.dump(
                    nx.readwrite.json_graph.node_link_data(graph, edges="edges"),
                    file,
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

    def explore(self) -> None:
        """
        Provides an interactive exploration of the knowledge graph in the users browser
        """
        with socketserver.TCPServer(
            ("", constants.LOCAL_FILE_HOSTING_PORT),
            functools.partial(
                http.server.SimpleHTTPRequestHandler,
                directory=str(self._local_alg_dir),
            ),
        ) as httpd:
            try:
                logger.info(
                    "Launching knowledge graph explorer" + "\n    (<ctrl+c> to stop)"
                )
                webbrowser.open(
                    f"http://localhost:{constants.LOCAL_FILE_HOSTING_PORT}/explore_knowledge_graph.html"
                )
                httpd.serve_forever()
            except KeyboardInterrupt:
                logger.info("Server stopped")
