"""Gitlab CICD Python Wrapper - Pydantic models for GitLab CI/CD YAML."""

__version__ = "0.1.0"

from gitlab_cicd_python_wrapper._async import AsyncComponent, AsyncPipeline
from gitlab_cicd_python_wrapper.artifacts import ArtifactReports, Artifacts
from gitlab_cicd_python_wrapper.cache import Cache, CacheKey
from gitlab_cicd_python_wrapper.common import (
    ArtifactAccess,
    ArtifactWhen,
    AutoCancelOnJobFailure,
    AutoCancelOnNewCommit,
    CachePolicy,
    CacheWhen,
    DeploymentTier,
    EnvironmentAction,
    InputType,
    RetryWhen,
    WhenCondition,
)
from gitlab_cicd_python_wrapper.component import Component
from gitlab_cicd_python_wrapper.environment import Environment
from gitlab_cicd_python_wrapper.globals import AutoCancel, Default, Workflow
from gitlab_cicd_python_wrapper.image import Image, Service
from gitlab_cicd_python_wrapper.include import (
    ComponentReference,
    IncludeComponent,
    IncludeItem,
    IncludeLocal,
    IncludeProject,
    IncludeRemote,
    IncludeTemplate,
)
from gitlab_cicd_python_wrapper.job import AllowFailure, Inherit, Job, Parallel
from gitlab_cicd_python_wrapper.needs import Need, NeedsPipeline
from gitlab_cicd_python_wrapper.pages import Pages
from gitlab_cicd_python_wrapper.pipeline import Pipeline
from gitlab_cicd_python_wrapper.release import Release
from gitlab_cicd_python_wrapper.retry import Retry
from gitlab_cicd_python_wrapper.rules import Rule, WorkflowRule
from gitlab_cicd_python_wrapper.secrets import Secret, VaultConfig, VaultEngine
from gitlab_cicd_python_wrapper.spec import ComponentInput, ComponentSpec, InputRule
from gitlab_cicd_python_wrapper.trigger import Trigger, TriggerForward
from gitlab_cicd_python_wrapper.variables import Variable

__all__ = [
    "AllowFailure",
    "ArtifactAccess",
    "ArtifactReports",
    "ArtifactWhen",
    "Artifacts",
    "AsyncComponent",
    "AsyncPipeline",
    "AutoCancel",
    "AutoCancelOnJobFailure",
    "AutoCancelOnNewCommit",
    "Cache",
    "CacheKey",
    "CachePolicy",
    "CacheWhen",
    "Component",
    "ComponentInput",
    "ComponentReference",
    "ComponentSpec",
    "Default",
    "DeploymentTier",
    "Environment",
    "EnvironmentAction",
    "Image",
    "IncludeComponent",
    "IncludeItem",
    "IncludeLocal",
    "IncludeProject",
    "IncludeRemote",
    "IncludeTemplate",
    "Inherit",
    "InputRule",
    "InputType",
    "Job",
    "Need",
    "NeedsPipeline",
    "Pages",
    "Parallel",
    "Pipeline",
    "Release",
    "Retry",
    "RetryWhen",
    "Rule",
    "Secret",
    "Service",
    "Trigger",
    "TriggerForward",
    "Variable",
    "VaultConfig",
    "VaultEngine",
    "WhenCondition",
    "Workflow",
    "WorkflowRule",
]
