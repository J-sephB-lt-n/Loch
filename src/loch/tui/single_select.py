"""
This buggy rubbish code was produced almost entirely by GPT-4o mini - it needs to
be completely rewritten.

docstring TODO
"""

from blessed import Terminal


def launch_single_select(options: list[str], unselectable: list[str] = []) -> str:
    """
    This buggy rubbish code was produced almost entirely by GPT-4o mini - it needs to
    be completely rewritten.

    Allows the user to select a single option in the terminal.
    Options marked as unselectable will be visible but greyed out and skipped by the cursor.

    Args:
        options (list[str]): List of available options for selection.
        unselectable (list[str]): List of options that should not be selectable.

    Returns:
        str: The selected option.
    """
    for item in unselectable:
        if item not in options:
            raise ValueError(
                f"item '{item}' in `unselectable` does not appear in `options`",
            )
    term = Terminal()
    cursor = 0

    instruction = (
        "Select an option (use ↑ ↓ to navigate, Enter to select, 'q' to quit):"
    )

    def draw():
        print(term.clear())
        print(term.bold_underline(instruction) + "\n")

        for i, opt in enumerate(options):
            is_unselectable = opt in unselectable
            if is_unselectable:
                # Display unselectable options in grey
                line = f"[ ] {term.color(8)}{opt}{term.normal}"
            else:
                # Display selectable options normally
                line = f"[{'x' if i == cursor else ' '}] {opt}"

            if i == cursor and not is_unselectable:
                print(term.reverse(line))  # Highlight the selected option
            else:
                print(line)

    with term.cbreak(), term.hidden_cursor():
        draw()
        while True:
            key = term.inkey()

            if key.code == term.KEY_UP:
                cursor = (cursor - 1) % len(options)
                # Skip unselectable options
                while options[cursor] in unselectable:
                    cursor = (cursor - 1) % len(options)
            elif key.code == term.KEY_DOWN:
                cursor = (cursor + 1) % len(options)
                # Skip unselectable options
                while options[cursor] in unselectable:
                    cursor = (cursor + 1) % len(options)
            elif key.code in (term.KEY_ENTER, term.KEY_RETURN):
                if options[cursor] not in unselectable:
                    return options[cursor]  # Immediately return after selection
            elif key.lower() == "q":  # Quick exit
                exit()

            draw()


if __name__ == "__main__":
    selected_option: str = launch_single_select(
        options=["joe", "is", "the", "worst", "best"],
        unselectable=["worst"],
    )
    print(selected_option)
