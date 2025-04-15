from pathlib import Path
from typing import Final

AVAILABLE_QUERY_ALGS: Final[list[str]] = [
    "Semantic Search",
    "BM25",
    "LLM Raw Content Question-Answering",
    "Auto-tagging",
    "Agentic Knowledge Distillation (Pyramid Search)",
    "LLM-Generated Knowledge Graph",
]

LOCAL_PROJECT_PATH: Final[Path] = Path("./.loch")
LOCAL_DATABASES_PATH: Final[Path] = LOCAL_PROJECT_PATH / "databases"
VECTOR_DB_NAME: Final[str] = "local-vector-db"
VECTOR_DB_PATH: Final[Path] = LOCAL_DATABASES_PATH / VECTOR_DB_NAME

DEFAULT_SEMANTIC_EMBEDDING_MODEL_NAME: Final[str] = "minishlab/potion-base-8M"
