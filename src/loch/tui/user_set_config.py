"""
CLI interfaces for user to set various configs
"""

import getpass
import json
from pathlib import Path

from loch.constants import LOCAL_LLM_MODELS_PATH


def get_llm_config_from_user() -> dict:
    """
    Get LLM params from user, saving them to project config (so can be reused)
    """
    last_llm_config_filepath: Path = LOCAL_LLM_MODELS_PATH / "last_llm_config.json"
    llm_config: dict
    if not last_llm_config_filepath.exists():
        llm_config = {
            "base_url": input("Please provide LLM API base URL: "),
            "api_key": getpass.getpass(
                "Please provide LLM API key (can leave blank for Ollama): "
            ),
            "model_name": input("Please provide LLM model name: "),
            "temperature": float(input("Please provide LLM model temperature: ")),
        }
        with open(last_llm_config_filepath, "w") as file:
            json.dump(
                llm_config,
                file,
                indent=4,
            )
        return llm_config

    with open(last_llm_config_filepath, "r") as file:
        last_llm_config: dict = json.load(file)

    llm_config = {}

    base_url: str = input(
        "Please provide LLM API base URL "
        + f"(leave blank to use previous '{last_llm_config['base_url']}'): "
    ).strip()
    llm_config["base_url"] = base_url or last_llm_config["base_url"]

    api_key: str = input(
        "Please provide LLM API key " + "(leave blank to use previous value): "
    ).strip()
    llm_config["api_key"] = api_key or last_llm_config["api_key"]

    model_name: str = input(
        "Please provide LLM model name "
        + f"(leave blank to use previous '{last_llm_config['model_name']}'): "
    ).strip()
    llm_config["model_name"] = model_name or last_llm_config["model_name"]

    temperature: str = input(
        "Please provide LLM model temperature "
        + f"(leave blank to use previous '{last_llm_config['temperature']}'): "
    ).strip()
    if len(temperature) > 0:
        llm_config["temperature"] = float(temperature)
    else:
        llm_config["temperature"] = last_llm_config["temperature"]

    if llm_config != last_llm_config:
        with open(last_llm_config_filepath, "r") as file:
            last_llm_config: dict = json.load(file)

    return llm_config
