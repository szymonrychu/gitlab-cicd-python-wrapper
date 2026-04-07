from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from gitlab_cicd_python_wrapper.common import ArtifactAccess, ArtifactWhen


class ArtifactReports(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    junit: list[str] | str | None = None
    coverage_report: dict[str, str] | None = None
    codequality: list[str] | str | None = None
    sast: list[str] | str | None = None
    dependency_scanning: list[str] | str | None = None
    container_scanning: list[str] | str | None = None
    dast: list[str] | str | None = None
    license_scanning: list[str] | str | None = None
    performance: list[str] | str | None = None
    dotenv: list[str] | str | None = None
    terraform: list[str] | str | None = None
    metrics: list[str] | str | None = None
    requirements: list[str] | str | None = None
    secret_detection: list[str] | str | None = None
    cyclonedx: list[str] | str | None = None


class Artifacts(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    paths: list[str] | None = None
    exclude: list[str] | None = None
    expire_in: str | None = None
    expose_as: str | None = None
    name: str | None = None
    public: bool | None = None
    access: ArtifactAccess | None = None
    reports: ArtifactReports | None = None
    untracked: bool | None = None
    when: ArtifactWhen | None = None
