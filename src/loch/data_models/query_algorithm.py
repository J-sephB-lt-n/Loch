from typing import Literal, Protocol


class QueryAlgorithm(Protocol):
    """
    An algorithm which can be used to query file content
    """

    def setup(self, step: Literal["index", "query"]) -> None:
        """
        Prepare (initialise) the algorithm for use

        Args:
            step:   step="index" processes all files for efficient future querying.
                    step="query" prepares the algorithm to process a user query.
        """
        ...

    def query_interface(self) -> None:
        """
        Runs an interactive interface which gets a query from the user and processes it
        """
        ...
