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


class TestWhenCondition:
    def test_values(self):
        assert WhenCondition.on_success == "on_success"
        assert WhenCondition.on_failure == "on_failure"
        assert WhenCondition.always == "always"
        assert WhenCondition.never == "never"
        assert WhenCondition.manual == "manual"
        assert WhenCondition.delayed == "delayed"

    def test_member_count(self):
        assert len(WhenCondition) == 6


class TestCachePolicy:
    def test_values(self):
        assert CachePolicy.pull == "pull"
        assert CachePolicy.push == "push"
        assert CachePolicy.pull_push == "pull-push"

    def test_member_count(self):
        assert len(CachePolicy) == 3


class TestCacheWhen:
    def test_values(self):
        assert CacheWhen.on_success == "on_success"
        assert CacheWhen.on_failure == "on_failure"
        assert CacheWhen.always == "always"

    def test_member_count(self):
        assert len(CacheWhen) == 3


class TestArtifactWhen:
    def test_values(self):
        assert ArtifactWhen.on_success == "on_success"
        assert ArtifactWhen.on_failure == "on_failure"
        assert ArtifactWhen.always == "always"

    def test_member_count(self):
        assert len(ArtifactWhen) == 3


class TestArtifactAccess:
    def test_values(self):
        assert ArtifactAccess.all == "all"
        assert ArtifactAccess.developer == "developer"
        assert ArtifactAccess.maintainer == "maintainer"
        assert ArtifactAccess.none == "none"

    def test_member_count(self):
        assert len(ArtifactAccess) == 4


class TestRetryWhen:
    def test_values(self):
        assert RetryWhen.always == "always"
        assert RetryWhen.unknown_failure == "unknown_failure"
        assert RetryWhen.script_failure == "script_failure"
        assert RetryWhen.api_failure == "api_failure"
        assert RetryWhen.stuck_or_timeout_failure == "stuck_or_timeout_failure"
        assert RetryWhen.runner_system_failure == "runner_system_failure"
        assert RetryWhen.missing_dependency_failure == "missing_dependency_failure"
        assert RetryWhen.runner_unsupported == "runner_unsupported"
        assert RetryWhen.stale_schedule == "stale_schedule"
        assert RetryWhen.job_execution_timeout == "job_execution_timeout"
        assert RetryWhen.archived_failure == "archived_failure"
        assert RetryWhen.unmet_prerequisites == "unmet_prerequisites"
        assert RetryWhen.scheduler_failure == "scheduler_failure"
        assert RetryWhen.data_integrity_failure == "data_integrity_failure"

    def test_member_count(self):
        assert len(RetryWhen) == 14


class TestDeploymentTier:
    def test_values(self):
        assert DeploymentTier.production == "production"
        assert DeploymentTier.staging == "staging"
        assert DeploymentTier.testing == "testing"
        assert DeploymentTier.development == "development"
        assert DeploymentTier.other == "other"

    def test_member_count(self):
        assert len(DeploymentTier) == 5


class TestEnvironmentAction:
    def test_values(self):
        assert EnvironmentAction.start == "start"
        assert EnvironmentAction.stop == "stop"
        assert EnvironmentAction.prepare == "prepare"
        assert EnvironmentAction.rollback == "rollback"

    def test_member_count(self):
        assert len(EnvironmentAction) == 4


class TestAutoCancelOnNewCommit:
    def test_values(self):
        assert AutoCancelOnNewCommit.conservative == "conservative"
        assert AutoCancelOnNewCommit.interruptible == "interruptible"
        assert AutoCancelOnNewCommit.none == "none"

    def test_member_count(self):
        assert len(AutoCancelOnNewCommit) == 3


class TestAutoCancelOnJobFailure:
    def test_values(self):
        assert AutoCancelOnJobFailure.all == "all"
        assert AutoCancelOnJobFailure.none == "none"

    def test_member_count(self):
        assert len(AutoCancelOnJobFailure) == 2


class TestInputType:
    def test_values(self):
        assert InputType.string == "string"
        assert InputType.number == "number"
        assert InputType.boolean == "boolean"
        assert InputType.array == "array"

    def test_member_count(self):
        assert len(InputType) == 4
