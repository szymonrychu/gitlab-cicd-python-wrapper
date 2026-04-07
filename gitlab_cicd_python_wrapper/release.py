from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Release(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    tag_name: str
    description: str
    name: str | None = None
    ref: str | None = None
    milestones: list[str] | None = None
    released_at: str | None = None
