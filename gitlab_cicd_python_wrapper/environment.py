from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from gitlab_cicd_python_wrapper.common import DeploymentTier, EnvironmentAction


class EnvironmentKubernetesDashboard(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    namespace: str | None = Field(None, min_length=1)
    flux_resource_path: str | None = None


class EnvironmentKubernetesManagedResources(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    enabled: bool | None = None


class EnvironmentKubernetes(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    agent: str | None = None
    dashboard: EnvironmentKubernetesDashboard | None = None
    managed_resources: EnvironmentKubernetesManagedResources | None = None
    # Deprecated in GitLab 18.4 in favour of dashboard:namespace / dashboard:flux_resource_path.
    namespace: str | None = Field(None, min_length=1)
    flux_resource_path: str | None = None


class Environment(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    name: str = Field(min_length=1)
    url: str | None = None
    on_stop: str | None = None
    action: EnvironmentAction | None = None
    auto_stop_in: str | None = None
    kubernetes: EnvironmentKubernetes | None = None
    deployment_tier: DeploymentTier | None = None
