"""
Core logic of the code run when the user calls `loch explore`
"""

from loch.algs import ALGS
from loch import tui
from loch.constants import (
    LOCAL_PROJECT_PATH,
    ALG_NAMES,
)


def loch_explore():
    if not LOCAL_PROJECT_PATH.exists():
        print(f"No [loch] project found in directory '{LOCAL_PROJECT_PATH}'")
        print("Run `loch init` to create a new project")
        exit()

    selected_query_alg_name: str = ALG_NAMES.findkey(
        tui.launch_single_select(
            options=ALG_NAMES.values,
        )
    )

    query_alg = ALGS[selected_query_alg_name]

    query_alg.explore()
