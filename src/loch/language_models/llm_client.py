"""
A client for interacting with Large Language Models via HTTP
"""

import httpx


class LLM:
    def __init__(
        self,
        api_base_url: str,
        api_key: str,
    ) -> None:
        self._api_client = openai.OpenAI(api_base_url, api_key)

    def chat(
        self,
        stream: bool,
        prompt_messages: list[dict],
        print_to_stdout: bool = False,
    ) -> str:
        """x"""
        return "TODO"
