from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from gitlab_cicd_python_wrapper.common import WhenCondition


class Rule(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    if_: str | None = Field(None, alias="if")
    changes: list[str] | None = None
    exists: list[str] | None = None
    when: WhenCondition | None = None
    allow_failure: bool | None = None
    variables: dict[str, str] | None = None
    start_in: str | None = None


class WorkflowRule(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    if_: str | None = Field(None, alias="if")
    changes: list[str] | None = None
    exists: list[str] | None = None
    when: WhenCondition | None = None
    variables: dict[str, str] | None = None
    auto_cancel: dict | None = None
