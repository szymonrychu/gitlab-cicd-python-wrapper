from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from gitlab_cicd_python_wrapper.artifacts import Artifacts
from gitlab_cicd_python_wrapper.cache import Cache
from gitlab_cicd_python_wrapper.common import IdentityProvider
from gitlab_cicd_python_wrapper.image import Image, Service
from gitlab_cicd_python_wrapper.retry import Retry, RetryMax
from gitlab_cicd_python_wrapper.rules import AutoCancel, WorkflowRule
from gitlab_cicd_python_wrapper.script import Hooks, Script
from gitlab_cicd_python_wrapper.secrets import IdToken

__all__ = ["AutoCancel", "Default", "Workflow"]


class Default(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    after_script: Script | None = None
    artifacts: Artifacts | None = None
    before_script: Script | None = None
    cache: Cache | list[Cache] | None = None
    hooks: Hooks | None = None
    id_tokens: dict[str, IdToken] | None = None
    identity: IdentityProvider | None = None
    image: str | Image | None = None
    interruptible: bool | None = None
    retry: RetryMax | Retry | None = None
    services: list[str | Service] | None = None
    tags: list[str | list[str]] | None = None
    timeout: str | None = None


class Workflow(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    name: str | None = None
    rules: list[WorkflowRule] | None = None
    auto_cancel: AutoCancel | None = None
