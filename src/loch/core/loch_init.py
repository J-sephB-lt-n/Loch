"""
Core logic of the code run when the user calls `loch init`
"""

from loch import constants

def loch_init():
    if constants.LOCAL_PROJECT_PATH.exists():
        print(
            f"Existing [loch] project found in directory '{constants.LOCAL_PROJECT_PATH}'"
        )
        print("Run `loch cleanup` to delete the existing project")
        exit()

    constants.LOCAL_PROJECT_PATH.mkdir()
    constants.LOCAL_DATABASES_PATH.mkdir()
