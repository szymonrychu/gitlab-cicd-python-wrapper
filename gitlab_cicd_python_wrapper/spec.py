from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from gitlab_cicd_python_wrapper.common import InputType


class InputRule(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    if_: str = Field(alias="if")
    options: list[str | int | float | bool] | None = None
    default: str | int | float | bool | list | None = None


class ComponentInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    type: InputType = InputType.string
    default: str | int | float | bool | list | None = None
    description: str | None = None
    options: list[str | int | float | bool] | None = None
    regex: str | None = None
    rules: list[InputRule] | None = None

    @model_validator(mode="after")
    def validate_default_in_options(self) -> ComponentInput:
        if self.options is not None and self.default is not None:
            if self.default not in self.options:
                raise ValueError(f"default {self.default!r} must be one of options {self.options!r}")
        return self

    @model_validator(mode="after")
    def validate_regex_only_for_string(self) -> ComponentInput:
        if self.regex is not None and self.type != InputType.string:
            raise ValueError("regex is only valid for type 'string'")
        return self


class ComponentSpec(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    description: str | None = None
    inputs: dict[str, ComponentInput] | None = None
    include: list[dict[str, Any]] | None = None
    component: list[str] | None = None

    @field_validator("inputs")
    @classmethod
    def inputs_not_empty(cls, v: dict[str, ComponentInput] | None) -> dict[str, ComponentInput] | None:
        if v is not None and len(v) == 0:
            raise ValueError("spec:inputs cannot be empty")
        return v
