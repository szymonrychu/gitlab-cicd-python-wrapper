from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from gitlab_cicd_python_wrapper.common import RetryWhen

# GitLab allows at most 2 retries (3 attempts in total).
RetryMax = Annotated[int, Field(ge=0, le=2)]


class Retry(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    max: RetryMax | None = None
    when: RetryWhen | list[RetryWhen] | None = None
    exit_codes: int | list[int] | None = None
