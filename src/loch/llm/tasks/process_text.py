"""
docstring TODO
"""

from loch.data_models import LlmClientInterface
from loch.llm import prompts


def process_text(
    input_text: str,
    processing_instructions: str,
    llm: LlmClientInterface,
) -> str:
    """
    Process `input_text` according to `processing_instructions` using model `llm`
    """
    return llm.chat(
        messages=[
            {
                "role": "user",
                "content": prompts.process_text.render(
                    input_text=input_text.strip(),
                    processing_instructions=processing_instructions.strip(),
                ),
            },
        ]
    )
