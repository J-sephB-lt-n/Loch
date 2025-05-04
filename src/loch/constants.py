from pathlib import Path
from typing import Final

from loch.utils.data_structures import BiMap

ALG_NAMES: Final[BiMap] = BiMap(
    # TODO: should use the registry pattern here
    # refer also to algs/__init__.py
    [
        # ("code_review", "Code Review"),
        ("entire_doc_vector_search", "Entire Document Vector Search (semantic & BM25)"),
        ("llm_auto_tagging", "LLM-Generated Auto-Tagging"),
        ("llm_knowledge_graph", "LLM-Generated Knowledge Graph"),
        ("llm_question_answering", "LLM Content Question-Answering"),
        ("pyramid_search", "Agentic Knowledge Distillation (Pyramid Search)"),
        (
            "pyamid_search_with_search_agent",
            "Agentic Knowledge Distillation (Pyramid Search) with Search Agent",
        ),
        ("semantic_code_search", "Semantic Code Search"),
    ],
)

LOCAL_PROJECT_PATH: Final[Path] = Path("./.loch")
LOCAL_ALG_CONFIGS_PATH: Final[Path] = LOCAL_PROJECT_PATH / "alg_configs"
LOCAL_DATABASES_PATH: Final[Path] = LOCAL_PROJECT_PATH / "databases"
LOCAL_MODELS_PATH: Final[Path] = LOCAL_PROJECT_PATH / "models"
LOCAL_EMBEDDING_MODELS_PATH: Final[Path] = LOCAL_MODELS_PATH / "embeddings"
LOCAL_LLM_MODELS_PATH: Final[Path] = LOCAL_MODELS_PATH / "llms"
VECTOR_DB_NAME: Final[str] = "local-vector-db"
VECTOR_DB_PATH: Final[Path] = LOCAL_DATABASES_PATH / VECTOR_DB_NAME

DEFAULT_MODEL2VEC_MODEL: Final[str] = "minishlab/potion-base-8M"
