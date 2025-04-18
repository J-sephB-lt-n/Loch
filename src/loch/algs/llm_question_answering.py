"""
docstring TODO
"""

from typing import Literal

from loch.data_models.query_algorithm import QueryAlgorithm
from loch.llm.client import global_llm_client


class LlmQuestionAnswering(QueryAlgorithm):
    """
    Generative language model answers user questions about text content
    """

    def setup(self, step: Literal["index", "query"]) -> None:
        """
        Prepare (initialise) the algorithm for use

        Args:
            step:   step="index" processes all files for efficient future querying.
                    step="query" prepares the algorithm to process a user query.
        """
        if step == "index":
            self._llm_client = global_llm_client
            self._llm_client.initialise_if_not_initialised()

        summarize_instruction: str = input(
            "Describe how you would like each document to be summarised"
            + "\n(leave blank to include file contents in full): "
        )
        print("llm_question_answering is not yet implemented")

    def query(self) -> None:
        """
        Runs an interactive interface which gets a query from the user and processes it
        """
        print("llm_question_answering is not yet implemented")
