from pathlib import Path
from typing import Any, Literal, Optional, Protocol


class QueryAlgorithm(Protocol):
    """
    An algorithm which can be used to query text
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
            filepaths:  List of files to process (used by `step`=='index')
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

    def explore(self) -> None:
        """
        Provides an interactive or visual exploration of the algorithm's data structures,
        allowing users to understand and navigate through the indexed content.
        """
        ...
