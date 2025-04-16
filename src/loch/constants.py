from pathlib import Path
from typing import Final

from loch.common.data_structures import BiMap

ALG_NAMES: Final[BiMap] = BiMap(
    [
        ("fts_bm25", "Full-Text Search (BM25)"),
        ("llm_auto_tagging", "LLM-Generated Auto-Tagging"),
        ("llm_knowledge_graph", "LLM-Generated Knowledge Graph"),
        ("llm_question_answering", "LLM Content Question-Answering"),
        ("pyramid_search", "Agentic Knowledge Distillation (Pyramid Search)"),
        ("semantic_search", "Semantic Search"),
    ],
)

LOCAL_PROJECT_PATH: Final[Path] = Path("./.loch")
LOCAL_ALG_CONFIGS_PATH: Final[Path] = LOCAL_PROJECT_PATH / "alg_configs"
LOCAL_DATABASES_PATH: Final[Path] = LOCAL_PROJECT_PATH / "databases"
VECTOR_DB_NAME: Final[str] = "local-vector-db"
VECTOR_DB_PATH: Final[Path] = LOCAL_DATABASES_PATH / VECTOR_DB_NAME

DEFAULT_SEMANTIC_EMBEDDING_MODEL_NAME: Final[str] = "minishlab/potion-base-8M"
