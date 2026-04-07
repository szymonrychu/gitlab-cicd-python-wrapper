from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from gitlab_cicd_python_wrapper.common import RetryWhen


class Retry(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    max: int = Field(ge=0, le=5)
    when: list[RetryWhen] | None = None
