from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from gitlab_cicd_python_wrapper.common import ReleaseLinkType


class ReleaseLink(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    name: str = Field(min_length=1)
    url: str = Field(min_length=1)
    filepath: str | None = None
    link_type: ReleaseLinkType | None = None


class ReleaseAssets(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    links: list[ReleaseLink] = Field(min_length=1)


class Release(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    tag_name: str
    tag_message: str | None = None
    description: str
    name: str | None = None
    ref: str | None = None
    milestones: list[str] | None = None
    released_at: str | None = None
    assets: ReleaseAssets | None = None
