"""
Functions for working with the `https://github.com/MinishLab/model2vec` embedding model
"""

import logging
from pathlib import Path

import model2vec

from loch import constants
from loch.utils.logging_utils import get_logger

logger: logging.Logger = get_logger(__name__)

MODEL2VEC_DOWNLOAD_DIR: Path = constants.LOCAL_EMBEDDING_MODELS_PATH / "model2vec"

if not MODEL2VEC_DOWNLOAD_DIR.exists():
    logger.info(
        f"Downloading model2vec model `{constants.DEFAULT_MODEL2VEC_MODEL}` to `{MODEL2VEC_DOWNLOAD_DIR}`"
    )
    MODEL2VEC_DOWNLOAD_DIR.mkdir()
    embed_model = model2vec.StaticModel.from_pretrained(constants.DEFAULT_MODEL2VEC_MODEL)
    embed_model.save_pretrained(MODEL2VEC_DOWNLOAD_DIR)
else:
    logger.info(
        f"Loading previously downloaded model2vec model `{constants.DEFAULT_MODEL2VEC_MODEL}` from `{MODEL2VEC_DOWNLOAD_DIR}`"
    )
    embed_model = model2vec.StaticModel.from_pretrained(MODEL2VEC_DOWNLOAD_DIR)
