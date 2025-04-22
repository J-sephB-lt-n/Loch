"""
Clients for interacting with the vector database

I could definitely make this code more abstracted/interfacey but I just want to experiment \
quickly with embeddings
"""

from pathlib import Path

import lancedb

from loch import constants


class LanceDbClient:
    def __init__(
        self,
        db_path: Path,
    ) -> None:
        self._db_path: Path = db_path
        self._db_conn = lancedb.connect(
            constants.VECTOR_DB_PATH,
        )
        self._table_conns: dict = {}

    def create_table(
        self,
        table_name: str,
        data: list[dict],
        add_full_text_search_index: bool = False,
    ) -> None:
        """
        Create a table and add vectors
        """
        for item in data:
            if "vector" not in item or "text" not in item:
                raise ValueError(
                    "items in `data` must contain (at a minimum) the keys ['vector', 'text']"
                )

        self._table_conns[table_name] = self._db_conn.create_table(
            table_name,
            data=data,
        )

        if add_full_text_search_index:
            self._table_conns[table_name].create_fts_index(
                "text",
                use_tantivy=False,
            )

    def semantic_search(
        self, table_name: str, search_query_embedding: list[float], top_k: int
    ) -> list[dict]:
        if table_name not in self._table_conns:
            self._table_conns[table_name] = self._db_conn.open_table(table_name)

        return (
            self._table_conns[table_name]
            .search(search_query_embedding)
            .limit(top_k)
            .to_list()
        )

    def full_text_search(
        self, table_name: str, search_query: str, top_k: int
    ) -> list[dict]:
        if table_name not in self._table_conns:
            self._table_conns[table_name] = self._db_conn.open_table(table_name)

        return self._table_conns[table_name].search(search_query).limit(top_k).to_list()

    def hybrid_search(
        self,
        table_name: str,
        search_query_embedding: list[float],
        search_query: str,
        top_k: int,
    ) -> list[dict]:
        if table_name not in self._table_conns:
            self._table_conns[table_name] = self._db_conn.open_table(table_name)

        return (
            self._table_conns[table_name]
            .search(query_type="hybrid")
            .vector(search_query_embedding)
            .text(search_query)
            .limit(top_k)
            .to_list()
        )
