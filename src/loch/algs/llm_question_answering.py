"""
docstring TODO
"""

from pathlib import Path
from typing import Final, Literal, Optional

from tqdm import tqdm

from loch import constants
from loch.data_models.query_algorithm import QueryAlgorithm
from loch.llm.client import global_llm_client
from loch.llm import prompts


class LlmQuestionAnswering(QueryAlgorithm):
    """
    Generative language model answers user questions about text content
    """

    def __init__(self) -> None:
        self._processed_files_contents: Optional[str] = None

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
                "Describe how you would like each document to be summarised/processed."
                + "\n(leave blank to include file contents in full): "
            ).strip()
            with open(
                (
                    constants.LOCAL_ALG_CONFIGS_PATH
                    / "llm_question_answering"
                    / "processing_instructions.txt"
                ),
                "w",
            ) as file:
                file.write(
                    f"""
<processing-instructions>
{processing_instructions}
</processing_instructions>
                    """.strip()
                )

            for filepath in tqdm(filepaths):
                tqdm.write(f"Processing {filepath}")
                with open(filepath, "r") as file:
                    if processing_instructions:
                        text = self._llm_client.chat(
                            messages=[
                                {
                                    "role": "user",
                                    "content": prompts.process_text.render(
                                        input_text=file.read().strip(),
                                        processing_instructions=processing_instructions,
                                    ),
                                },
                            ]
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

        elif step == "query":
            with open(PROCESSED_FILE_CONTENTS_FILEPATH, "r") as file:
                self._processed_files_contents = file.read()

    def query(
        self,
        user_query: str,
        verbose: bool = False,
    ) -> str:
        """
        Retrieve results most relevant to `user_query`

        Args:
            user_query (str): Query to generate results for
            verbose (bool): If true, model response is streamed to stdout
        """
        if not self._processed_files_contents:
            raise RuntimeError(
                "LlmQuestionAnswering algorithm is not ready for querying."
                + 'Please run LlmQuestionAnswering.setup(step="query")'
            )
        llm_response: str = self._llm_client.chat(
            messages=[
                {
                    "role": "user",
                    "content": prompts.query_processed_file_contents.render(
                        user_query=user_query,
                        processed_file_contents=self._processed_files_contents,
                    ),
                }
            ],
            stream=verbose,
        )
        return llm_response

    def launch_query_interface(self) -> None:
        """
        Runs an interactive interface which gets a query from the user and processes it
        """
        while True:
            user_query: str = input(
                "Please enter your question " + "(submit 'exit' to quit): \n"
            ).strip()
            if user_query == "exit":
                print(" ...exiting LlmQuestionAnswering query interface")
                return
            _ = self.query(
                user_query=user_query,
                verbose=True,
            )
            print("\n-----------------------------------\n")
