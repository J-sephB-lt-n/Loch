from typing import Any, Literal, Protocol


class QueryAlgorithm(Protocol):
    """
    An algorithm which can be used to query text
    """

    def setup(
        self,
        step: Literal["index", "query"],
    ) -> None:
        """
        Prepare (initialise) the algorithm for use

        Args:
            step:   step="index" processes all files for efficient future querying.
                    step="query" prepares the algorithm to process a user query.
        """
        ...

    def query(self, user_query: str) -> Any:
        """
        Retrieve results most relevant to `user_query`
        """
        ...

    def launch_query_interface(self) -> None:
        """
        Runs an interactive interface for user querying
        """
        ...
