from __future__ import annotations

from enum import Enum


class WhenCondition(str, Enum):
    on_success = "on_success"
    on_failure = "on_failure"
    always = "always"
    never = "never"
    manual = "manual"
    delayed = "delayed"


class CachePolicy(str, Enum):
    pull = "pull"
    push = "push"
    pull_push = "pull-push"


class CacheWhen(str, Enum):
    on_success = "on_success"
    on_failure = "on_failure"
    always = "always"


class ArtifactWhen(str, Enum):
    on_success = "on_success"
    on_failure = "on_failure"
    always = "always"


class ArtifactAccess(str, Enum):
    all = "all"
    developer = "developer"
    maintainer = "maintainer"
    none = "none"


class RetryWhen(str, Enum):
    always = "always"
    unknown_failure = "unknown_failure"
    script_failure = "script_failure"
    api_failure = "api_failure"
    stuck_or_timeout_failure = "stuck_or_timeout_failure"
    runner_system_failure = "runner_system_failure"
    missing_dependency_failure = "missing_dependency_failure"
    runner_unsupported = "runner_unsupported"
    stale_schedule = "stale_schedule"
    job_execution_timeout = "job_execution_timeout"
    archived_failure = "archived_failure"
    unmet_prerequisites = "unmet_prerequisites"
    scheduler_failure = "scheduler_failure"
    data_integrity_failure = "data_integrity_failure"


class DeploymentTier(str, Enum):
    production = "production"
    staging = "staging"
    testing = "testing"
    development = "development"
    other = "other"


class EnvironmentAction(str, Enum):
    start = "start"
    stop = "stop"
    prepare = "prepare"
    rollback = "rollback"


class AutoCancelOnNewCommit(str, Enum):
    conservative = "conservative"
    interruptible = "interruptible"
    none = "none"


class AutoCancelOnJobFailure(str, Enum):
    all = "all"
    none = "none"


class InputType(str, Enum):
    string = "string"
    number = "number"
    boolean = "boolean"
    array = "array"
