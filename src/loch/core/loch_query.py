"""
Core logic of the code run when the user calls `loch query`
"""

from loch.constants import LOCAL_PROJECT_PATH
from loch.data_models import ProjectConfig


def loch_query():
    with open(LOCAL_PROJECT_PATH / "project_config.json", "r") as file:
        project_config = ProjectConfig.model_validate_json(
            file.read(),
        )
