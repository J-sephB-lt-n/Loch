"""
docstring TODO
"""

import getpass
import json
import logging
from pathlib import Path
from typing import Final, Optional

import httpx
import openai

from loch.constants import LOCAL_LLM_MODELS_PATH
from loch.llm.tokenizers import count_approx_tokens
from loch.utils.logging_utils import get_logger

logger: logging.Logger = get_logger(__name__)


def get_default_llm_config() -> dict:
    """
    Get default LLM params and save to project config (so can be reused)
    """
    default_config_filepath: Path = LOCAL_LLM_MODELS_PATH / "default_llm_config.json"
    if not default_config_filepath.exists():
        with open(default_config_filepath, "w") as file:
            json.dump(
                {
                    "base_url": input("Please provide default LLM API base URL: "),
                    "api_key": getpass.getpass(
                        "Please provide default LLM API key (can leave blank for Ollama): "
                    ),
                    "model_name": input("Please provide default LLM model name: "),
                },
                file,
                indent=4,
            )
        logger.info(f"Default LLM config written to {default_config_filepath}")

    with open(default_config_filepath, "r") as file:
        logger.info(f"Default LLM config read from {default_config_filepath}")
        return json.load(file)


class LlmClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        model_name: str,
        temperature: float,
        logger: logging.Logger,
    ) -> None:
        self.base_url = base_url
        self.api_key = api_key
        self.model_name = model_name
        self.temperature = temperature
        self._logger = logger
        self._api_client = None
        if ":11434" in self.base_url:
            self._logger.info(
                "LLM client is assumed to be Ollama (discovered ':11434' in base_url)"
            )
            self.chat = self._ollama_chat
            self.api_spec = "ollama"
        else:
            self._logger.info("LLM client is assumed to be OpenAI API compatible")
            self.api_spec = "openai"
            self._api_client = openai.OpenAI(
                base_url=self.base_url,
                api_key=self.api_key,
            )
            self.chat = self._openai_chat

    def _ollama_chat(
        self,
        messages: list[dict] | None,
        stream: bool = False,
    ) -> str:
        OLLAMA_TIMEOUT: Final[int] = 5 * 60
        request_body: dict = {
            "model": self.model_name,
            "messages": messages,
            # "stream": False,
            "options": {
                "num_ctx": int(
                    count_approx_tokens(
                        model_name=self.model_name,
                        text=str(messages),
                    )
                    * 1.1
                ),  # adding 10% more for safety
                "temperature": self.temperature,
            },
        }
        if stream:
            full_response_text: str = ""
            with httpx.stream(
                "POST",
                url=f"{self.base_url}/api/chat",
                timeout=OLLAMA_TIMEOUT,
                json=request_body | {"stream": True},
            ) as response:
                line_json: Optional[dict] = None
                for line in response.iter_lines():
                    if not line:
                        continue
                    line_json = json.loads(line)
                    print(
                        line_json["message"]["content"],
                        end="",
                        flush=True,
                    )
                    full_response_text += line_json["message"]["content"]
            self._logger.info(
                json.dumps(
                    line_json,
                    indent=4,
                )
            )
            return full_response_text

        elif not stream:
            return httpx.post(
                url=f"{self.base_url}/api/chat",
                timeout=OLLAMA_TIMEOUT,
                json=request_body | {"stream": False},
            ).json()["message"]["content"]

    def _openai_chat(
        self,
        messages: list[dict],
        stream: bool = False,
    ) -> str:
        request_kwargs: dict = {
            "model": self.model_name,
            "timeout": 30,
            "messages": messages,
        }
        if stream:
            full_response_text: str = ""
            response_stream = self._api_client.chat.completions.create(
                stream=True,
                **request_kwargs,
            )
            for chunk in response_stream:
                chunk_text: Optional[str] = chunk.choices[0].delta.content
                if chunk_text is not None:
                    print(chunk_text, end="")
                    full_response_text += chunk_text
            return full_response_text
        elif not stream:
            return (
                self._api_client.chat.completions.create(
                    stream=False,
                    **request_kwargs,
                )
                .choices[0]
                .message.content
            )

    def preload_ollama_model(self, num_ctx: Optional[int] = None) -> None:
        """
        Preload the (Ollama) model
        """
        self._logger.info(f"Preloading ollama model [{self.model_name}]")
        request_body: dict = {
            "model": self.model_name,
            "options": {},
        }
        if num_ctx:
            request_body["options"]["num_ctx"] = num_ctx

        _ = httpx.post(
            url=f"{self.base_url}/api/chat",
            timeout=60,
            json=request_body,
        )


# class GlobalLlmClient:
#     """
#     Ensures that LLM client can be shared by multiple algs and can be \
#     lazily initialised (and only once)
#     """
#
#     def __init__(self):
#         self._is_initialised = False
#         self._llm_client = None
#         self.logger = get_logger(__name__)
#
#     def initialise_if_not_initialised(self):
#         if not self._is_initialised:
#             self._llm_client = LlmClient(
#                 base_url=input("Please provide LLM base URL: "),
#                 api_key=getpass.getpass(
#                     "Please provide LLM API key (can leave blank for Ollama): "
#                 ),
#                 model_name=input("Please provide LLM model name: "),
#                 temperature=float(input("Please provide LLM temperature: ")),
#                 logger=get_logger(__name__),
#             )
#             self._is_initialised = True
#             if self._llm_client.api_spec == "ollama":
#                 self.logger.info(
#                     f"Preloading the Ollama model '{self._llm_client.model_name}'"
#                 )
#                 self._llm_client.preload_model()
#
#     def chat(self, *args, **kwargs) -> str:
#         if not self._is_initialised:
#             raise RuntimeError("GlobalLlmClient has not been initialised yet")
#
#         return self._llm_client.chat(*args, **kwargs)
#
#
# global_llm_client = GlobalLlmClient()
