"""
Core logic of the code run when the user calls `loch init`
"""

import json
from pathlib import Path

import loch.data_models
from loch import constants, tui


def loch_init():
    if constants.LOCAL_PROJECT_PATH.exists():
        print(
            f"Existing [loch] project found in directory '{constants.LOCAL_PROJECT_PATH}'"
        )
        print("Run `loch cleanup` to delete the existing project")
        exit()

    constants.LOCAL_PROJECT_PATH.mkdir()
    constants.LOCAL_DATABASES_PATH.mkdir()

    selected_files: set[Path] = tui.launch_file_selector()
    print(selected_files)

    project_config = loch.data_models.ProjectConfig(
        algs={},
        searchable_files=selected_files,
    )

    with open(constants.LOCAL_PROJECT_PATH / "project_config.json", "w") as file:
        json.dump(
            project_config.model_dump(mode="json"),
            file,
            indent=4,
        )
