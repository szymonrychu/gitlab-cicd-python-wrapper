from __future__ import annotations

from enum import Enum


class WhenCondition(str, Enum):
    on_success = "on_success"
    on_failure = "on_failure"
    always = "always"
    never = "never"
    manual = "manual"
    delayed = "delayed"


class WorkflowWhen(str, Enum):
    always = "always"
    never = "never"


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
    stuck_pending_with_matching_runners = "stuck_pending_with_matching_runners"
    stuck_pending_no_matching_runners = "stuck_pending_no_matching_runners"
    no_updates_running = "no_updates_running"
    no_updates_canceling = "no_updates_canceling"
    runner_system_failure = "runner_system_failure"
    runner_configuration_error = "runner_configuration_error"
    runner_external_dependency_failure = "runner_external_dependency_failure"
    runner_interrupted = "runner_interrupted"
    missing_dependency_failure = "missing_dependency_failure"
    runner_unsupported = "runner_unsupported"
    stale_schedule = "stale_schedule"
    job_execution_timeout = "job_execution_timeout"
    server_timeout_running = "server_timeout_running"
    server_timeout_canceling = "server_timeout_canceling"
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
    verify = "verify"
    access = "access"


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


class PullPolicy(str, Enum):
    always = "always"
    never = "never"
    if_not_present = "if-not-present"


class TriggerStrategy(str, Enum):
    depend = "depend"
    mirror = "mirror"


class CoverageFormat(str, Enum):
    cobertura = "cobertura"
    jacoco = "jacoco"


class ReleaseLinkType(str, Enum):
    runbook = "runbook"
    package = "package"
    image = "image"
    other = "other"


class IdentityProvider(str, Enum):
    google_cloud = "google_cloud"


class InheritDefaultKeyword(str, Enum):
    after_script = "after_script"
    artifacts = "artifacts"
    before_script = "before_script"
    cache = "cache"
    image = "image"
    interruptible = "interruptible"
    retry = "retry"
    services = "services"
    tags = "tags"
    timeout = "timeout"
