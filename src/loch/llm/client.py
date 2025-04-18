import logging

import httpx

from loch.llm.tokenizers import count_approx_tokens
from loch.utils.logging_utils import get_logger


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
        if ":11434" in self.base_url:
            self._logger.info(
                "LLM client is assumed to be Ollama (discovered ':11434' in base_url)"
            )
            self.chat = self._ollama_chat
            self.api_spec = "ollama"
        else:
            self._logger.info("LLM client is assumed to be OpenAI API compatible")
            self.api_spec = "openai"
            self.chat = self._openai_chat

    def _ollama_chat(
        self,
        messages: list[dict] | None,
        stream: bool = False,
    ) -> str:
        if stream:
            raise NotImplementedError
        elif not stream:
            return httpx.post(
                url=f"{self.base_url}/api/chat",
                timeout=60,
                json={
                    "model": self.model_name,
                    "messages": messages,
                    "stream": False,
                    "num_ctx": count_approx_tokens(
                        model_name=self.model_name,
                        text=str(messages),
                    ),
                },
            ).json()

    def _openai_chat(
        self,
        messages: list[dict],
        stream: bool = False,
    ) -> str:
        raise NotImplementedError

    def preload_model(self) -> None:
        """
        Preload the (Ollama) model
        """
        _ = httpx.post(
            url=f"{self.base_url}/api/chat",
            timeout=60,
            json={
                "model": self.model_name,
            },
        )


class GlobalLlmClient:
    """
    Ensures that LLM client can be shared by multiple processes and can be lazily initialised (and only once)
    """

    def __init__(self):
        self._is_initialised = False
        self._llm_client = None
        self.logger = get_logger(__name__)

    def initialise_if_not_initialised(self):
        if not self._is_initialised:
            self._llm_client = LlmClient(
                base_url=input("Please provide LLM base URL: "),
                api_key=input(
                    "Please provide LLM API key (can leave blank for Ollama): "
                ),
                model_name=input("Please provide LLM model name: "),
                temperature=float(input("Please provide LLM temperature: ")),
                logger=get_logger(__name__),
            )
            self._is_initialised = True
            if self._llm_client.api_spec == "ollama":
                self.logger.info(
                    f"Preloading the Ollama model '{self._llm_client.model_name}'"
                )
                self._llm_client.preload_model()

    def chat(self, *args, **kwargs) -> str:
        if not self._is_initialised:
            raise RuntimeError("GlobalLlmClient has not been initialised yet")

        return self._llm_client.chat(*args, **kwargs)


global_llm_client = GlobalLlmClient()
