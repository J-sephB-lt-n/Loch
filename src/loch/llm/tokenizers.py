"""
Functions related to tokenisation
"""


def count_approx_tokens(model_name: str, text: str) -> int:
    """
    Count approximate number of tokens in `text` for the given model
    """
    if model_name[:6] == "gemma3":
        return int(len(text) / 4)
    else:
        raise ValueError(
            f"Counting tokens for model '{model_name}' not currently supported"
        )
