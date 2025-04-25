"""
Functions for working with the `https://github.com/MinishLab/model2vec` embedding model
"""

import logging
from pathlib import Path

import model2vec

from loch import constants
from loch.utils.logging_utils import get_logger

logger: logging.Logger = get_logger(__name__)


class GlobalModel2VecClient:
    """
    Class used to lazily load model2vec, and ensure it can be reused without reinitialising it
    """

    def __init__(self) -> None:
        self._model2vec_download_dir: Path = (
            constants.LOCAL_EMBEDDING_MODELS_PATH / "model2vec"
        )
        self.embed_model = None

    def initialise_if_not_initialised(self) -> None:
        if self.embed_model is None:
            if not self._model2vec_download_dir.exists():
                logger.info(
                    f"Downloading model2vec model `{constants.DEFAULT_MODEL2VEC_MODEL}` to `{self._model2vec_download_dir}`"
                )
                self._model2vec_download_dir.mkdir(parents=True)
                self.embed_model = model2vec.StaticModel.from_pretrained(
                    constants.DEFAULT_MODEL2VEC_MODEL
                )
                self.embed_model.save_pretrained(self._model2vec_download_dir)
            else:
                logger.info(
                    f"Loading previously downloaded model2vec model `{constants.DEFAULT_MODEL2VEC_MODEL}` from `{self._model2vec_download_dir}`"
                )
                self.embed_model = model2vec.StaticModel.from_pretrained(
                    self._model2vec_download_dir
                )


model2vec_client = GlobalModel2VecClient()
