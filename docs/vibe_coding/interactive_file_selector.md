
My python CLI app requires users to select files from their local filesystem.

Please write me a python function which does the following:

- Launches a TUI (terminal user interface)

- This TUI allows the user to effectively select files from the local filesystem

- The TUI screen is split in half

- The left side of the TUI screen shows a filetree of the current directory, looking like the ouput of the linux `tree` package.

i.e. like this: 

```
src
└── loch
    ├── __init__.py
    ├── cli.py
    ├── constants.py
    ├── databases.py
    ├── filesystem.py
    ├── language_models
    │   ├── llm_client.py
    │   └── semantic_vector_embedding.py
    ├── llm_prompts.py
    ├── main.py
    ├── py.typed
    └── search.py
```

- The filetree view excludes any paths which include a dot folder or a leading-underscore-named folder in any part of the path

- The user can navigate up and down in this filetree using their up and down arrow arrow keys i.e. the user cursor will be on one of the files or folders at any given time. If the filetree output is longer than the users screen, then it must scroll with the position of the user cursor (e.g. like the linux `less` command). 

- The right hand side of the TUI screen shows the contents of the file which the user cursor is currently on. The user can scroll up and down this file contents view using their `j` (down) and `k` (up) keys.

- Pressing enter (return) key adds the file which the cursor is currently on to the set of selected files. Pressing enter (return) on a file already in the set of selected files removes (deselects) it.

- All selected files appear as highlighted in the filetree view using tickboxes on the left hand side of the screen.

- Pressing enter (return) key on a folder adds it and all of the files and folders within it (recursively all the way down) to the current set of selected files. Pressing enter (return) on a folder which is already part of the set of selected files/folders removes it and all of the files and folders within it from the set of selected files/folders.

- At the top left of the screen (above the filetree), the following statistics are always shown (regardless of the scroll position of the filetree):

  - Number of files in selection

  - Total number of lines in selection

  - Total number of words in selection

- Use the python blessed library
