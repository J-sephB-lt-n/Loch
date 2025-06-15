"""
LLM answers questions about provided text
"""

import logging
from pathlib import Path
from typing import Final, Literal, Optional

from tqdm import tqdm

from loch import constants
from loch.data_models.query_algorithm import QueryAlgorithm

from loch.llm import prompts
from loch.llm.client import LlmClient
from loch.llm.tokenizers import count_approx_tokens
from loch.tui import get_llm_config_from_user
from loch.utils.logging_utils import get_logger

logger: logging.Logger = get_logger(__name__)


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

        self.llm_config = get_llm_config_from_user()
        self._llm_client = LlmClient(
            base_url=self.llm_config["base_url"],
            api_key=self.llm_config["api_key"],
            model_name=self.llm_config["model_name"],
            temperature=self.llm_config["temperature"],
            logger=logger,
        )

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

            if self._llm_client.api_spec == "ollama":
                logger.info(
                    "Calculating largest included file size in order to load appropriate Ollama model"
                )
                max_required_tokens: int = 0
                for filepath in tqdm(filepaths):
                    tqdm.write(f"Reading {filepath}")
                    with open(filepath, "r") as file:
                        max_required_tokens = max(
                            max_required_tokens,
                            count_approx_tokens(
                                text=file.read(),
                                model_name=self._llm_client.model_name,
                            ),
                        )
                chosen_num_ctx: int = int(max_required_tokens * 1.1)
                self._llm_client.preload_ollama_model(num_ctx=chosen_num_ctx)

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
            if self._llm_client.api_spec == "ollama":
                logger.info("Preloading Ollama model with required context window size")
                chosen_num_ctx: int = int(
                    1.1
                    * count_approx_tokens(
                        text=self._processed_files_contents,
                        model_name=self._llm_client.model_name,
                    ),
                )
                self._llm_client.preload_ollama_model(num_ctx=chosen_num_ctx)

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

    def explore(self) -> None:
        """
        Provides an interactive exploration of the processed file contents.
        """
        print("explore() method not implemented")
