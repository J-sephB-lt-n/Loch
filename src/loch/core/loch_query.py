"""
Core logic of the code run when the user calls `loch query`
"""

from loch.constants import ALG_NAMES, LOCAL_PROJECT_PATH
from loch.data_models import ProjectConfig
from loch.tui import launch_single_select


def loch_query():
    with open(LOCAL_PROJECT_PATH / "project_config.json", "r") as file:
        project_config = ProjectConfig.model_validate_json(
            file.read(),
        )

    chosen_alg: str = launch_single_select(
        options=list(project_config.algs.keys()),
        unselectable=[
            alg_name
            for alg_name, is_selectable in project_config.algs.items()
            if not is_selectable
        ],
    )
    assert chosen_alg in ALG_NAMES.keys

    print(chosen_alg)
