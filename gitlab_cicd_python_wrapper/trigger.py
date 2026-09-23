from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from gitlab_cicd_python_wrapper.common import TriggerStrategy


class TriggerForward(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    yaml_variables: bool | None = None
    pipeline_variables: bool | None = None


class Trigger(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    project: str | None = None
    branch: str | None = None
    strategy: TriggerStrategy | None = None
    include: str | list[dict[str, Any]] | None = Field(None, max_length=3)
    inputs: dict[str, Any] | None = None
    forward: TriggerForward | None = None

    @model_validator(mode="after")
    def project_or_include(self) -> Trigger:
        if self.project is not None and self.include is not None:
            raise ValueError("trigger:project and trigger:include are mutually exclusive")
        if self.branch is not None and self.project is None:
            raise ValueError("trigger:branch requires trigger:project")
        return self
