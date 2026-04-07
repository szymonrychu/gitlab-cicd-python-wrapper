from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from gitlab_cicd_python_wrapper.common import CachePolicy, CacheWhen


class CacheKey(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    files: list[str] | None = None
    files_commits: list[str] | None = None
    prefix: str | None = None


class Cache(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    paths: list[str] | None = None
    key: str | CacheKey | None = None
    untracked: bool | None = None
    unprotect: bool | None = None
    when: CacheWhen | None = None
    policy: CachePolicy | None = None
    fallback_keys: list[str] | None = None
