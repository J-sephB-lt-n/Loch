"""
Functions for working with the `https://github.com/MinishLab/model2vec` embedding model
"""

import logging
from pathlib import Path

from loch import constants
from loch.utils.logging_utils import get_logger

logger: logging.Logger = get_logger(__name__)

model2vec_download_dir: Path = constants.LOCAL_EMBEDDING_MODELS_PATH / "model2vec"

if not model2vec_download_dir.exists():
    logger.info(
        f"Downloading model2vec model `{constants.DEFAULT_MODEL2VEC_MODEL}` to `{model2vec_download_dir}`"
    )
    model2vec_download_dir.mkdir()
