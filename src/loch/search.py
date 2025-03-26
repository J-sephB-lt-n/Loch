import json

import lancedb

from loch import constants
from loch.cli import get_user_input_from_fixed_options
from loch.language_models.semantic_vector_embedding import (
    create_semantic_vector_embedding_model,
)


def run_search() -> None:
    """
    Run the user search interface
    """
    with open(constants.LOCAL_PROJECT_PATH / "config.json", "r") as file:
        config: dict = json.load(file)

    available_search_methods = [
        method_name
        for method_name, is_available in config["available_search_methods"].items()
        if is_available
    ]

    if (
        "semantic vector search" in available_search_methods
        or "keyword search (bm25)" in available_search_methods
    ):
        print("Connecting to vector database")
        vector_db = lancedb.connect(constants.VECTOR_DB_PATH)
        vector_db_table = vector_db.open_table("vector_search")

    # if "semantic vector search" in available_search_methods:
    #     print("Loading embedding model")
    #     embed_model = create_semantic_vector_embedding_model(
    #         model_name=constants.DEFAULT_SEMANTIC_EMBEDDING_MODEL_NAME,
    #     )

    while True:
        print("Please select a search method")
        user_choice: str = get_user_input_from_fixed_options(
            options=available_search_methods + ["exit"]
        )
        if user_choice == "exit":
            exit()
        print(f"Search method '{user_choice}' selected")
        user_query: str = input("Please enter your search query: ")

        if user_choice in (
            "semantic vector search",
            "keyword search (bm25)",
            "hybrid search (semantic + bm25)",
        ):
            search_results = (
                vector_db_table.search(
                    user_query,
                    query_type={
                        "semantic vector search": "vector",
                        "keyword search (bm25)": "fts",
                        "hybrid search (semantic + bm25)": "hybrid",
                    }.get(user_choice),
                )
                .select(
                    [
                        "filepath",
                    ]
                )
                .limit(10)
                .to_list()
            )

            for result in search_results:
                print(
                    json.dumps(
                        result,
                        indent=4,
                    )
                )

        print("\nStarting a new search")
