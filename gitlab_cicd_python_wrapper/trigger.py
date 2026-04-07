from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class TriggerForward(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    yaml_variables: bool | None = None
    pipeline_variables: bool | None = None
    dotenv_variables: bool | None = None


class Trigger(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    project: str | None = None
    branch: str | None = None
    strategy: str | None = None
    include: list[dict[str, Any]] | None = None
    forward: TriggerForward | None = None
