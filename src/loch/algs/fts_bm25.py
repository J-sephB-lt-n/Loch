"""
docstring TODO
"""

from typing import Literal

from loch.data_models.query_algorithm import QueryAlgorithm

class FtsBm25(QueryAlgorithm):
    """
    Full-Text Search using BM25 
    """

    def setup(self, step: Literal["index", "query"]) -> None:
        """
        Prepare (initialise) the algorithm for use

        Args:
            step:   step="index" processes all files for efficient future querying.
                    step="query" prepares the algorithm to process a user query.
        """
        print("fts_bm25 is not yet implemented")

    def query(self) -> None:
        """
        Runs an interactive interface which gets a query from the user and processes it
        """
        print("fts_bm25 is not yet implemented")
