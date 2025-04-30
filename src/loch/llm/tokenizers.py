"""
Functions related to tokenisation
"""

import logging

from loch.utils.logging_utils import get_logger

logger: logging.Logger = get_logger(__name__)


def count_approx_tokens(model_name: str, text: str) -> int:
    """
    Count approximate number of tokens in `text` for the given model
    """
    if model_name[:6] == "gemma3":
        logger.info("Model is 'gemma3' - using heuristic '4 characters per token'")
        return int(len(text) / 4)
    else:
        logger.warning(
            f"No token counting approach available for model '{model_name}'"
            + " - using heuristic '3 characters per token'"
        )
        return int(len(text) / 3)
