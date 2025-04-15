"""
Core run when the user calls `loch cleanup`
"""

import shutil

from loch import constants


def loch_cleanup():
    """Completely deletes the loch project in the current folder"""
    if not constants.LOCAL_PROJECT_PATH.exists():
        print(f"No local project found at '{constants.LOCAL_PROJECT_PATH}'")
        exit()

    user_confirmation = input(
        "Are you sure that you want to completely the [loch] project in the current folder?\n"
        + "(anything response other than 'yes' will abort): "
    )
    if user_confirmation == "yes":
        shutil.rmtree(constants.LOCAL_PROJECT_PATH)
        print("[loch] project deleted")
    else:
        print("...process cancelled by user")
