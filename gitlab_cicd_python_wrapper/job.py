from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from gitlab_cicd_python_wrapper.artifacts import Artifacts
from gitlab_cicd_python_wrapper.cache import Cache
from gitlab_cicd_python_wrapper.common import (
    IdentityProvider,
    InheritDefaultKeyword,
    InputType,
    WhenCondition,
)
from gitlab_cicd_python_wrapper.environment import Environment
from gitlab_cicd_python_wrapper.image import Image, Service
from gitlab_cicd_python_wrapper.needs import (
    MatrixValue,
    Need,
    NeedsPipeline,
    NeedsProject,
)
from gitlab_cicd_python_wrapper.pages import Pages
from gitlab_cicd_python_wrapper.release import Release
from gitlab_cicd_python_wrapper.retry import Retry, RetryMax
from gitlab_cicd_python_wrapper.rules import Rule
from gitlab_cicd_python_wrapper.script import Hooks, Script
from gitlab_cicd_python_wrapper.secrets import IdToken, Secret
from gitlab_cicd_python_wrapper.trigger import Trigger
from gitlab_cicd_python_wrapper.variables import (
    VariableValue,
    reject_global_only_variable_keys,
)


class AllowFailure(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    exit_codes: list[int] | int


class DastConfiguration(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    site_profile: str | None = None
    scanner_profile: str | None = None


class Inherit(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    default: bool | list[InheritDefaultKeyword] | None = None
    variables: bool | list[str] | None = None


class Parallel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    matrix: list[dict[str, MatrixValue]] = Field(max_length=200)


class Step(BaseModel):
    """A single entry of the experimental `run` keyword (CI/CD functions)."""

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    name: str
    script: str | None = None
    step: str | dict[str, Any] | None = None
    func: str | dict[str, Any] | None = None
    env: dict[str, str] | None = None
    inputs: dict[str, Any] | None = None

    @model_validator(mode="after")
    def exactly_one_action(self) -> Step:
        actions = [a for a in ("script", "step", "func") if getattr(self, a) is not None]
        if len(actions) != 1:
            raise ValueError(f"run step {self.name!r} must define exactly one of script, step or func")
        if self.script is not None and self.inputs is not None:
            raise ValueError(f"run step {self.name!r}: 'inputs' is only valid with 'step' or 'func'")
        return self


class JobInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    default: str | int | float | bool | list
    type: InputType = InputType.string
    description: str | None = Field(None, max_length=1024)
    options: list[str | int | float | bool] | None = None
    regex: str | None = None

    @model_validator(mode="after")
    def validate_default(self) -> JobInput:
        expected = {
            InputType.string: str,
            InputType.number: (int, float),
            InputType.boolean: bool,
            InputType.array: list,
        }[self.type]
        # bool is a subclass of int, so it must not satisfy `number`.
        if not isinstance(self.default, expected) or (self.type == InputType.number and isinstance(self.default, bool)):
            raise ValueError(f"default {self.default!r} does not match input type {self.type.value!r}")
        if self.options is not None and self.default not in self.options:
            raise ValueError(f"default {self.default!r} must be one of options {self.options!r}")
        if self.regex is not None and self.type != InputType.string:
            raise ValueError("regex is only valid for type 'string'")
        return self


class Filter(BaseModel):
    """Deprecated `only` / `except` hash form."""

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    refs: list[str] | None = None
    variables: list[str] | None = None
    changes: list[str] | None = None
    kubernetes: str | None = None

    @field_validator("kubernetes")
    @classmethod
    def kubernetes_active(cls, v: str | None) -> str | None:
        if v is not None and v != "active":
            raise ValueError("only/except:kubernetes supports only 'active'")
        return v


class Job(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    script: Script | None = None
    before_script: Script | None = None
    after_script: Script | None = None
    run: list[Step] | None = None
    stage: str | None = None
    image: str | Image | None = None
    services: list[str | Service] | None = None
    variables: dict[str, VariableValue] | None = None
    inputs: dict[str, JobInput] | None = Field(None, max_length=50)
    rules: list[Rule] | None = None
    only: list[str] | Filter | None = None
    except_: list[str] | Filter | None = Field(None, alias="except")
    allow_failure: bool | AllowFailure | None = None
    artifacts: Artifacts | None = None
    cache: Cache | list[Cache] | None = None
    needs: list[str | Need | NeedsPipeline | NeedsProject] | None = None
    tags: list[str | list[str]] | None = None
    when: WhenCondition | None = None
    environment: str | Environment | None = None
    extends: str | list[str] | None = None
    dependencies: list[str] | None = None
    coverage: str | None = None
    retry: RetryMax | Retry | None = None
    timeout: str | None = None
    parallel: int | Parallel | None = None
    trigger: str | Trigger | None = None
    resource_group: str | None = None
    interruptible: bool | None = None
    start_in: str | None = None
    release: Release | None = None
    secrets: dict[str, Secret] | None = None
    pages: bool | Pages | None = None
    publish: str | None = None  # Deprecated: use pages.publish
    inherit: Inherit | None = None
    dast_configuration: DastConfiguration | None = None
    identity: IdentityProvider | None = None
    manual_confirmation: str | None = None
    id_tokens: dict[str, IdToken] | None = None
    hooks: Hooks | None = None

    @field_validator("parallel")
    @classmethod
    def parallel_bounds(cls, v: int | Parallel | None) -> int | Parallel | None:
        if isinstance(v, int) and not 1 <= v <= 200:
            raise ValueError("parallel must be between 1 and 200")
        return v

    @field_validator("variables")
    @classmethod
    def job_variables_keys(cls, v: dict[str, VariableValue] | None) -> dict[str, VariableValue] | None:
        reject_global_only_variable_keys(v, "job")
        return v

    @model_validator(mode="after")
    def run_excludes_scripts(self) -> Job:
        if self.run is not None and any(s is not None for s in (self.script, self.before_script, self.after_script)):
            raise ValueError("'run' cannot be combined with 'script', 'before_script' or 'after_script'")
        return self
