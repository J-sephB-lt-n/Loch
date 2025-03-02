from pathlib import Path
from typing import Final

LOCAL_PROJECT_PATH: Final[Path] = Path("./loch")
LOCAL_DATABASES_PATH: Final[Path] = LOCAL_PROJECT_PATH / "databases"
VECTOR_DB_NAME: Final[str] = "local-vector-db"
VECTOR_DB_PATH: Final[Path] = LOCAL_DATABASES_PATH / VECTOR_DB_NAME

DEFAULT_SEMANTIC_EMBEDDING_MODEL_NAME: Final[str] = "mixedbread-ai/mxbai-embed-large-v1"
