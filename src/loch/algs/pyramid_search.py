"""
docstring TODO
"""

from pathlib import Path
from typing import Literal, Optional

from loch.data_models.query_algorithm import QueryAlgorithm


class PyramidSearch(QueryAlgorithm):
    """
    https://towardsdatascience.com/overcome-failing-document-ingestion-rag-strategies-with-agentic-knowledge-distillation/
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

    def query(self) -> None:
        """
        Runs an interactive interface which gets a query from the user and processes it
        """
        print("pyramid_search is not yet implemented")
