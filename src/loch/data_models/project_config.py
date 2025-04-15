"""
Definition of the project config data model
"""

import datetime
from pathlib import Path

import pydantic


class ProjectConfig(pydantic.BaseModel):
    project_created_at: datetime.datetime = pydantic.Field(
        default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc)
    )
    algs: dict[str, bool] = pydantic.Field(
        ...,
        description="Mapping of algorithm names to boolean values indicating inclusion (e.g. 'BM25': True)",
    )
    searchable_files: list[Path] = pydantic.Field(
        ...,
        description="Files included in project (i.e. files whose content can be queried/searched)",
    )
