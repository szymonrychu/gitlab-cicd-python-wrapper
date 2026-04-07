from __future__ import annotations

from typing import Any, Union

from pydantic import BaseModel, ConfigDict


class ComponentReference(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    fqdn: str
    project_path: str
    component_name: str
    version: str

    @classmethod
    def from_string(cls, ref: str) -> ComponentReference:
        base, version = ref.split("@", 1)
        parts = base.split("/")
        return cls(
            fqdn=parts[0],
            component_name=parts[-1],
            project_path="/".join(parts[1:-1]),
            version=version,
        )


class IncludeLocal(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    local: str
    inputs: dict[str, Any] | None = None
    rules: list[dict[str, Any]] | None = None


class IncludeRemote(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    remote: str
    inputs: dict | None = None
    rules: list[dict] | None = None
    integrity: str | None = None
    cache: bool | str | None = None


class IncludeTemplate(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    template: str
    inputs: dict | None = None


class IncludeProject(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    project: str
    file: str | list[str] | None = None
    ref: str | None = None
    inputs: dict | None = None
    rules: list[dict] | None = None


class IncludeComponent(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    component: str
    inputs: dict | None = None
    rules: list[dict] | None = None

    @property
    def parsed_ref(self) -> ComponentReference:
        return ComponentReference.from_string(self.component)


IncludeItem = Union[IncludeLocal, IncludeRemote, IncludeTemplate, IncludeProject, IncludeComponent]
