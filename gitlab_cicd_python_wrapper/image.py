from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Image(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    name: str
    entrypoint: list[str] | str | None = None
    pull_policy: str | None = None


class Service(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    name: str
    alias: str | None = None
    entrypoint: list[str] | str | None = None
    command: list[str] | str | None = None
    pull_policy: str | None = None
    variables: dict[str, str] | None = None
