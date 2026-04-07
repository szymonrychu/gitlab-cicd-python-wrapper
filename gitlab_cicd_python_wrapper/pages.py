from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Pages(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    publish: str | None = None
    expire_in: str | None = None
