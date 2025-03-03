"""
TAGS: bar|complete|completed|percent|percentage|progress|progress-bar|tqdm
DESCRIPTION: Basic progress bar printed to stdout
"""

import sys
import time


def print_progress_bar(
    iteration_num: int, final_iteration_num: int, bar_len: int = 50
) -> None:
    """Prints a progress bar to stdout

    Notes:
        - % completed is calculated as `iteration_num`/`final_iteration_num`
        - This allows you to index as you wish i.e. you can using 0-indexing
            or 1-indexing, depending on how you want the bar to be drawn

    Args:
        iteration_num (int): Number of current step
        final_iteration_num (int): Number of last step (i.e. after this step process is completed)
        bar_len (int): Total character length of the progress bar

    Example:
        >>> import time
        >>> n_steps: int = 27
        >>> print_progress_bar(0, n_steps, 50)
        >>> for i in range(0, n_steps):
        ...     time.sleep(0.2)
        ...     print_progress_bar(i+1, n_steps, 50)
    """
    percent_complete: float = iteration_num / final_iteration_num
    n_chars_filled: int = int(percent_complete * bar_len)
    progress_bar: str = "█" * n_chars_filled + "░" * (bar_len - n_chars_filled)

    sys.stdout.write(
        f"\r|{progress_bar}| {iteration_num}/{final_iteration_num} ({100 * percent_complete:.2f}%)"
    )
    sys.stdout.flush()

    if iteration_num == final_iteration_num:
        print()

def get_user_input_from_fixed_options(options: list[str]) -> str:
    """Get user input, not letting them proceed until they choose one of the allowed options"""
    options_map: dict[str, str] = {
        str(option_num): option
        for option_num, option in enumerate(options, start=1)
    }
    while True:
        print("Please select one of the following:")
        for option_num, option in options_map.items():
            print(f"\t({option_num}) {option}")
        print(
            "(enter one of {", 
            ",".join(options_map.keys()),
            "})",
            sep="",
        )
        selected: str = input()
        if selected in options_map.keys():
            return options_map[selected]
        else:
            print(
                f"Invalid selection '{selected}'"
            )


if __name__ == "__main__":
    n_steps: int = 27
    print_progress_bar(0, n_steps, 50)
    for i in range(0, n_steps):
        time.sleep(0.5)
        print_progress_bar(i + 1, n_steps, 50)
