from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator

from gitlab_cicd_python_wrapper.common import (
    AutoCancelOnJobFailure,
    AutoCancelOnNewCommit,
    WhenCondition,
    WorkflowWhen,
)
from gitlab_cicd_python_wrapper.variables import ScalarValue


class _PathsOrRegexp(BaseModel):
    @model_validator(mode="after")
    def exactly_one_of_paths_or_regexp(self):
        if (self.paths is None) == (self.regexp is None):
            raise ValueError("exactly one of 'paths' or 'regexp' must be set")
        return self


class RuleChanges(_PathsOrRegexp):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    paths: list[str] | None = None
    regexp: str | None = Field(None, max_length=255)
    compare_to: str | None = None


class RuleExists(_PathsOrRegexp):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    paths: list[str] | None = None
    regexp: str | None = Field(None, max_length=255)
    project: str | None = None
    ref: str | None = None

    @model_validator(mode="after")
    def ref_requires_project(self) -> RuleExists:
        if self.ref is not None and self.project is None:
            raise ValueError("rules:exists:ref requires rules:exists:project")
        return self


class RuleNeed(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    job: str = Field(min_length=1)
    artifacts: bool | None = None
    optional: bool | None = None


class AutoCancel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    on_new_commit: AutoCancelOnNewCommit | None = None
    on_job_failure: AutoCancelOnJobFailure | None = None


class Rule(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    if_: str | None = Field(None, alias="if")
    changes: list[str] | RuleChanges | None = None
    exists: list[str] | RuleExists | None = None
    when: WhenCondition | None = None
    allow_failure: bool | None = None
    needs: list[str | RuleNeed] | None = None
    variables: dict[str, ScalarValue] | None = None
    interruptible: bool | None = None
    start_in: str | None = None


class WorkflowRule(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    if_: str | None = Field(None, alias="if")
    changes: list[str] | RuleChanges | None = None
    exists: list[str] | RuleExists | None = None
    when: WorkflowWhen | None = None
    variables: dict[str, ScalarValue] | None = None
    auto_cancel: AutoCancel | None = None


class IncludeRule(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    if_: str | None = Field(None, alias="if")
    changes: list[str] | RuleChanges | None = None
    exists: list[str] | RuleExists | None = None
    when: WhenCondition | None = None
