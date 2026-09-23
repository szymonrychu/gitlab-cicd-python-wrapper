from __future__ import annotations

from typing import Union

from pydantic import BaseModel, ConfigDict, Field

MatrixValue = Union[str, int, float, list[Union[str, int, float]]]


class NeedParallel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    matrix: list[dict[str, MatrixValue]] = Field(max_length=200)


class Need(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    job: str
    artifacts: bool | None = None
    optional: bool | None = None
    parallel: NeedParallel | None = None


class NeedsPipeline(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    pipeline: str
    job: str
    artifacts: bool | None = None
    parallel: NeedParallel | None = None


class NeedsProject(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    project: str
    job: str
    ref: str
    artifacts: bool | None = None
    parallel: NeedParallel | None = None
