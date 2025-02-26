
import json

from loch import constants

def create_search_databases() -> None:
    with open(constants.LOCAL_PROJECT_PATH / "config.json", "r") as file:
        config: dict = json.load(file)

    if config["available_search_methods"]["semantic vector search"]:
        print("semantic vector search") 

    if config["available_search_methods"]["keyword search (bm25)"]:
        print("bm25")

