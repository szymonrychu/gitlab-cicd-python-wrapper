from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Need(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    job: str
    artifacts: bool | None = None
    optional: bool | None = None


class NeedsPipeline(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    pipeline: str
    job: str
    artifacts: bool | None = None
