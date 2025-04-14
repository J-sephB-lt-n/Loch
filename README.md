
# LOCH (LOcal searCH)

NEW PLAN!

`loch init` initialises a new project (fails if one already exists):

- first menu is file selector

- second menu is which search methods to create indexes for

- third method is setup for each selected method (loops through each and runs it's `setup(step="index")` method)

`loch query` opens a menu where you can select your method (from the available methods). Then,the `setup(step="query")` method is run, and then the `query()` method is run in a while loop.

`loch cleanup` deletes the project in the current folder (if there is one)

```bash
loch --help
loch init --dry_run

# it doesn't make sense to include all arguments at once,
#  but here are examples for all of them:
loch init --dry_run \
      --include_folders 'src' 'local files' \
      --exclude_folders '.venv' '.ruff-cache' '__pycache__' \
      --include_filetypes '.py' '.json' \
      --exclude_filetypes '.json' '.pdf' \
      --include_dot_folders \
      --include_leading_underscore_folders
loch init
loch search
loch clean
```

Future search approaches to explore:

- Graph database

- Semantic search/BM25 with chunking (there are many chunking methods)

- Tag-based search (with tags written by a local LLM)
