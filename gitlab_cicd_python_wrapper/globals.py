from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from gitlab_cicd_python_wrapper.artifacts import Artifacts
from gitlab_cicd_python_wrapper.cache import Cache
from gitlab_cicd_python_wrapper.common import (
    AutoCancelOnJobFailure,
    AutoCancelOnNewCommit,
)
from gitlab_cicd_python_wrapper.image import Image, Service
from gitlab_cicd_python_wrapper.retry import Retry
from gitlab_cicd_python_wrapper.rules import WorkflowRule


class Default(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    after_script: list[str] | None = None
    artifacts: Artifacts | None = None
    before_script: list[str] | None = None
    cache: Cache | list[Cache] | None = None
    hooks: dict[str, list[str]] | None = None
    id_tokens: dict[str, dict[str, str]] | None = None
    image: str | Image | None = None
    interruptible: bool | None = None
    retry: int | Retry | None = None
    services: list[str | Service] | None = None
    tags: list[str] | None = None


class AutoCancel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    on_new_commit: AutoCancelOnNewCommit | None = None
    on_job_failure: AutoCancelOnJobFailure | None = None


class Workflow(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    name: str | None = None
    rules: list[WorkflowRule] | None = None
    auto_cancel: AutoCancel | None = None
