from __future__ import annotations

from typing import Union

from pydantic import BaseModel, ConfigDict


class Variable(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    value: str
    description: str | None = None
    options: list[str] | None = None
    expand: bool | None = None


# GitLab accepts scalar variable values (strings, numbers, booleans) as well as the expanded hash form.
ScalarValue = Union[str, int, float, bool]
VariableValue = Union[str, int, float, bool, Variable]


def reject_global_only_variable_keys(variables: dict[str, VariableValue] | None, where: str) -> None:
    """`description` and `options` are only valid on global (pipeline-level) variables."""
    if not variables:
        return
    for name, var in variables.items():
        if isinstance(var, Variable) and (var.description is not None or var.options is not None):
            raise ValueError(
                f"{where} variable {name!r}: 'description' and 'options' are only allowed in global variables"
            )
