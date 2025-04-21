"""
docstring TODO
"""

from pathlib import Path
from typing import Literal, Optional

from loch.data_models.query_algorithm import QueryAlgorithm


class FtsBm25(QueryAlgorithm):
    """
    Full-Text Search using BM25
    """

    def setup(
        self, step: Literal["index", "query"], filepaths: Optional[list[Path]] = None
    ) -> None:
        """
        Prepare (initialise) the algorithm for use

        Args:
            step:   step="index" processes all files for efficient future querying.
                    step="query" prepares the algorithm to process a user query.
        """
        print("fts_bm25 is not yet implemented")

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
