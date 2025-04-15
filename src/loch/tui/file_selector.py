import os
from pathlib import Path

from blessed import Terminal

term = Terminal()


def is_valid_path(path: Path):
    return not any(part.startswith(".") or part.startswith("_") for part in path.parts)


def build_file_tree(base_path: Path):
    tree = []
    for root, dirs, files in os.walk(base_path):
        root_path = Path(root)
        if not is_valid_path(root_path.relative_to(base_path)):
            dirs[:] = []
            continue
        level = len(root_path.relative_to(base_path).parts)
        tree.append((root_path, level, True))
        for file in files:
            file_path = root_path / file
            if is_valid_path(file_path.relative_to(base_path)):
                tree.append((file_path, level + 1, False))
    return tree


def load_file_contents(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.readlines()
    except Exception:
        return ["[Unable to read file]"]


def launch_file_selector() -> list[Path]:
    base_path = Path(".").resolve()
    file_tree = build_file_tree(base_path)
    selected_files = set()
    cursor_index = 0
    file_scroll = 0

    def get_stats():
        line_count = 0
        word_count = 0
        for f in selected_files:
            try:
                with open(f, "r", encoding="utf-8") as file:
                    for line in file:
                        line_count += 1
                        word_count += len(line.split())
            except:
                continue
        return len(selected_files), line_count, word_count

    with term.fullscreen(), term.hidden_cursor(), term.cbreak():
        while True:
            height, width = term.height, term.width
            mid = width // 2
            visible_lines = height - 5  # Leave room for stats + instructions

            start = max(0, cursor_index - visible_lines // 2)
            end = min(len(file_tree), start + visible_lines)

            print(term.home + term.clear)

            # Top bar: Stats
            sel_count, total_lines, total_words = get_stats()
            print(
                term.move(0, 0)
                + f"Selected files: {sel_count} | Total lines: {total_lines} | Total words: {total_words}"
            )
            print(term.move(1, 0) + "-" * width)

            # Left: File tree
            for i in range(start, end):
                path, level, is_dir = file_tree[i]
                prefix = "📁" if is_dir else "📄"
                checkbox = "[x]" if path in selected_files else "[ ]"
                cursor = "➤" if i == cursor_index else "  "
                line = f"{cursor} {checkbox} {'  ' * level}{prefix} {path.name}"
                print(
                    term.move(i - start + 2, 0) + term.reverse(line)
                    if i == cursor_index
                    else line
                )

            # Right: File content
            curr_path, _, is_dir = file_tree[cursor_index]
            file_lines = (
                load_file_contents(curr_path) if not is_dir else ["[Directory]"]
            )
            for i, line in enumerate(
                file_lines[file_scroll : file_scroll + visible_lines]
            ):
                clipped = line[: mid - 1].rstrip()
                print(term.move(i + 2, mid) + clipped)

            # Bottom: Instructions
            instructions = (
                "↑/↓: Navigate  j/k: Scroll content  Enter: Select  q/Ctrl-G: Finish"
            )
            print(term.move(height - 2, 0) + term.reverse(instructions.center(width)))

            key = term.inkey()
            if key.code == term.KEY_UP:
                cursor_index = max(0, cursor_index - 1)
            elif key.code == term.KEY_DOWN:
                cursor_index = min(len(file_tree) - 1, cursor_index + 1)
            elif key == "j":
                file_scroll = min(len(file_lines) - 1, file_scroll + 1)
            elif key == "k":
                file_scroll = max(0, file_scroll - 1)
            elif key.code == term.KEY_ENTER or key == "\n":

                def toggle_selection(p):
                    if p in selected_files:
                        selected_files.discard(p)
                    else:
                        selected_files.add(p)

                path, _, is_dir = file_tree[cursor_index]
                if is_dir:
                    subtree = [
                        p for p, *_ in file_tree if p == path or p.is_relative_to(path)
                    ]
                    if path in selected_files:
                        selected_files.difference_update(subtree)
                    else:
                        selected_files.update(subtree)
                else:
                    toggle_selection(path)

            elif key == "q" or key.name == "KEY_ESCAPE":
                break

    return sorted([filepath for filepath in selected_files if not filepath.is_dir()])


def main():
    selected = launch_file_selector()
    print("\nSelected files:")
    for f in selected:
        print(f)
