"""
docstring TODO
"""

from typing import Literal

from loch.data_models.query_algorithm import QueryAlgorithm

class SemanticSearch(QueryAlgorithm):
    """
    Search over dense embedding vectors 
    """

    def setup(self, step: Literal["index", "query"]) -> None:
        """
        Prepare (initialise) the algorithm for use

        Args:
            step:   step="index" processes all files for efficient future querying.
                    step="query" prepares the algorithm to process a user query.
        """
        print("semantic_search is not yet implemented")

    def query(self) -> None:
        """
        Runs an interactive interface which gets a query from the user and processes it
        """
        print("semantic_search is not yet implemented")
