from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from gitlab_cicd_python_wrapper.common import DeploymentTier, EnvironmentAction


class EnvironmentKubernetes(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    namespace: str | None = None


class Environment(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    name: str
    url: str | None = None
    deployment_tier: DeploymentTier | None = None
    auto_stop_in: str | None = None
    action: EnvironmentAction | None = None
    kubernetes: EnvironmentKubernetes | None = None
