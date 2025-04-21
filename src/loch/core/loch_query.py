"""
Core logic of the code run when the user calls `loch query`
"""

from loch.constants import ALG_NAMES, LOCAL_PROJECT_PATH
from loch.data_models import ProjectConfig
from loch.tui import launch_single_select

from loch.algs import ALGS


def loch_query():
    with open(LOCAL_PROJECT_PATH / "project_config.json", "r") as file:
        project_config = ProjectConfig.model_validate_json(
            file.read(),
        )

    while True:
        # interface for user to choose a query algorithm #
        chosen_alg: str = launch_single_select(
            options=list(project_config.algs.keys()) + ["<EXIT>"],
            unselectable=[
                alg_name
                for alg_name, is_selectable in project_config.algs.items()
                if not is_selectable
            ],
        )
        assert chosen_alg in ALG_NAMES.keys + ["<EXIT>"]

        if chosen_alg == "<EXIT>":
            exit()

        # run the query interface of the chosen query algorithm #
        ALGS[chosen_alg].setup(step="query")
        ALGS[chosen_alg].launch_query_interface()
