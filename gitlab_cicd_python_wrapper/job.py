from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from gitlab_cicd_python_wrapper.artifacts import Artifacts
from gitlab_cicd_python_wrapper.cache import Cache
from gitlab_cicd_python_wrapper.common import WhenCondition
from gitlab_cicd_python_wrapper.environment import Environment
from gitlab_cicd_python_wrapper.image import Image, Service
from gitlab_cicd_python_wrapper.needs import Need, NeedsPipeline
from gitlab_cicd_python_wrapper.pages import Pages
from gitlab_cicd_python_wrapper.release import Release
from gitlab_cicd_python_wrapper.retry import Retry
from gitlab_cicd_python_wrapper.rules import Rule
from gitlab_cicd_python_wrapper.secrets import Secret
from gitlab_cicd_python_wrapper.trigger import Trigger
from gitlab_cicd_python_wrapper.variables import Variable


class AllowFailure(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    exit_codes: list[int] | int


class DastConfiguration(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    site_profile: str | None = None
    scanner_profile: str | None = None


class Identity(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    aud: str


class Inherit(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    default: bool | list[str] | None = None
    variables: bool | list[str] | None = None


class Parallel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    matrix: list[dict[str, list[str]]]


class RunConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    shell: str | None = None
    timeout: int | None = None


class Job(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    script: list[str] | None = None
    before_script: list[str] | None = None
    after_script: list[str] | None = None
    stage: str | None = None
    image: str | Image | None = None
    services: list[str | Service] | None = None
    variables: dict[str, str | Variable] | None = None
    rules: list[Rule] | None = None
    allow_failure: bool | AllowFailure | None = None
    artifacts: Artifacts | None = None
    cache: Cache | list[Cache] | None = None
    needs: list[str | Need | NeedsPipeline] | None = None
    tags: list[str] | None = None
    when: WhenCondition | None = None
    environment: str | Environment | None = None
    extends: str | list[str] | None = None
    dependencies: list[str] | None = None
    coverage: str | None = None
    retry: int | Retry | None = None
    timeout: str | None = None
    parallel: int | Parallel | None = None
    trigger: str | Trigger | None = None
    resource_group: str | None = None
    interruptible: bool | None = None
    start_in: str | None = None
    release: Release | None = None
    secrets: dict[str, Secret] | None = None
    pages: Pages | None = None
    inherit: Inherit | None = None
    dast_configuration: DastConfiguration | None = None
    identity: Identity | None = None
    manual_confirmation: str | None = None
    run: RunConfig | None = None
    id_tokens: dict[str, dict[str, str]] | None = None
    hooks: dict[str, list[str]] | None = None
