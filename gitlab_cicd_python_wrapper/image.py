from __future__ import annotations

from pydantic import BaseModel, ConfigDict, field_validator

from gitlab_cicd_python_wrapper.common import PullPolicy
from gitlab_cicd_python_wrapper.variables import (
    VariableValue,
    reject_global_only_variable_keys,
)


class ImageDocker(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    platform: str | None = None
    user: str | None = None


class ImageKubernetes(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    user: str | int | None = None


class Image(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    name: str
    entrypoint: list[str] | str | None = None
    docker: ImageDocker | None = None
    kubernetes: ImageKubernetes | None = None
    pull_policy: PullPolicy | list[PullPolicy] | None = None


class Service(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    name: str
    alias: str | None = None
    entrypoint: list[str] | str | None = None
    command: list[str] | str | None = None
    docker: ImageDocker | None = None
    kubernetes: ImageKubernetes | None = None
    pull_policy: PullPolicy | list[PullPolicy] | None = None
    variables: dict[str, VariableValue] | None = None

    @field_validator("variables")
    @classmethod
    def service_variables_keys(cls, v: dict[str, VariableValue] | None) -> dict[str, VariableValue] | None:
        reject_global_only_variable_keys(v, "service")
        return v
