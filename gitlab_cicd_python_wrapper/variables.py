from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Variable(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    value: str
    description: str | None = None
    options: list[str] | None = None
    expand: bool | None = None
