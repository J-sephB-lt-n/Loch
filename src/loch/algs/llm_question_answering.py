"""
docstring TODO
"""

from pathlib import Path
from typing import Final, Literal, Optional

from tqdm import tqdm

from loch import constants
from loch.data_models.query_algorithm import QueryAlgorithm
from loch.llm.client import global_llm_client
from loch.llm.tasks import process_text


class LlmQuestionAnswering(QueryAlgorithm):
    """
    Generative language model answers user questions about text content
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
        assert "llm_question_answering" in constants.ALG_NAMES.keys
        PROCESSED_FILE_CONTENTS_FILEPATH: Final[Path] = (
            constants.LOCAL_ALG_CONFIGS_PATH
            / "llm_question_answering"
            / "processed_file_contents.md"
        )

        self._llm_client = global_llm_client
        self._llm_client.initialise_if_not_initialised()

        if step == "index":
            processing_instructions: str = input(
                "Describe how you would like each document to be summarised/processed"
                + "\n(leave blank to include file contents in full): "
            ).strip()
            for filepath in tqdm(filepaths):
                tqdm.write(f"Processing {filepath}")
                with open(filepath, "r") as file:
                    if processing_instructions:
                        text = process_text(
                            input_text=file.read(),
                            processing_instructions=processing_instructions,
                            llm=self._llm_client,
                        )
                    else:
                        text = file.read()
                with open(PROCESSED_FILE_CONTENTS_FILEPATH, "a") as file:
                    file.write(
                        f"""
{filepath}
```
{text}                        
```
                        """
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
        print("llm_question_answering is not yet implemented")
