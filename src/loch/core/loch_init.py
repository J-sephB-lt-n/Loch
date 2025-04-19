"""
Core logic of the code run when the user calls `loch init`
"""

from pathlib import Path

from loch.algs import ALGS
import loch.data_models
from loch import tui
from loch.constants import (
    LOCAL_PROJECT_PATH,
    LOCAL_ALG_CONFIGS_PATH,
    LOCAL_DATABASES_PATH,
    ALG_NAMES,
)
from loch.utils.logging_utils import get_logger

logger = get_logger(__name__)


def loch_init():
    if LOCAL_PROJECT_PATH.exists():
        print(f"Existing [loch] project found in directory '{LOCAL_PROJECT_PATH}'")
        print("Run `loch cleanup` to delete the existing project")
        exit()

    LOCAL_PROJECT_PATH.mkdir()
    LOCAL_ALG_CONFIGS_PATH.mkdir()
    LOCAL_DATABASES_PATH.mkdir()

    selected_files: list[Path] = tui.launch_file_selector()
    selected_query_methods: list[str] = [
        ALG_NAMES.findkey(alg_name)
        for alg_name in tui.launch_multi_select(
            options=ALG_NAMES.values,
        )
    ]

    for alg_name in selected_query_methods:
        (LOCAL_ALG_CONFIGS_PATH / alg_name).mkdir()
        logger.info(f"Indexing files for algorithm [{alg_name}]")
        ALGS[alg_name].setup(step="index", filepaths=selected_files)

    project_config = loch.data_models.ProjectConfig(
        algs={
            alg_name: (alg_name in selected_query_methods)
            for alg_name in ALG_NAMES.keys
        },
        searchable_files=selected_files,
    )

    with open(LOCAL_PROJECT_PATH / "project_config.json", "w") as file:
        file.write(
            project_config.model_dump_json(indent=4),
        )
