from typing import Protocol


class LlmClientInterface(Protocol):
    def chat(self, *args, **kwargs) -> str: ...
