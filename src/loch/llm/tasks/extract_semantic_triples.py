"""
docstring TODO
"""

import json
import re

from loch.llm import prompts
from loch.llm.client import LlmClient


def extract_semantic_triples(
    text: str,
    llm: LlmClient,
) -> list[list[str]]:
    """
    Extract knowledge (RDF) triples from `text` using language model `llm`
    """
    llm_response: str = llm.chat(
        messages=[
            {
                "role": "user",
                "content": prompts.extract_semantic_triples.render(
                    document_contents=text,
                ),
            }
        ]
    )
    find_json = re.search(
        r"```json\s*(?P<json_content>.*?)```",
        llm_response,
        re.DOTALL,
    )
    if not find_json:
        raise ValueError("No JSON markdown code block found.")

    return json.loads(
        find_json.group("json_content").strip(),
    )
