
# LOCH (LOcal searCH)

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
