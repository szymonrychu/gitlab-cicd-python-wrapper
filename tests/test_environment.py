import pytest
from pydantic import ValidationError

from gitlab_cicd_python_wrapper.common import DeploymentTier, EnvironmentAction
from gitlab_cicd_python_wrapper.environment import Environment, EnvironmentKubernetes


class TestEnvironmentKubernetes:
    def test_create(self):
        k = EnvironmentKubernetes(namespace="production")
        assert k.namespace == "production"

    def test_empty(self):
        k = EnvironmentKubernetes()
        assert k.namespace is None

    def test_extra_forbidden(self):
        with pytest.raises(ValidationError):
            EnvironmentKubernetes(namespace="ns", foo="bar")


class TestEnvironment:
    def test_minimal(self):
        e = Environment(name="production")
        assert e.name == "production"
        assert e.url is None
        assert e.deployment_tier is None
        assert e.auto_stop_in is None
        assert e.action is None
        assert e.kubernetes is None

    def test_full(self):
        e = Environment(
            name="production",
            url="https://example.com",
            deployment_tier=DeploymentTier.production,
            auto_stop_in="1 week",
            action=EnvironmentAction.start,
            kubernetes=EnvironmentKubernetes(namespace="prod"),
        )
        assert e.url == "https://example.com"
        assert e.deployment_tier == DeploymentTier.production
        assert e.auto_stop_in == "1 week"
        assert e.action == EnvironmentAction.start
        assert e.kubernetes.namespace == "prod"

    def test_extra_forbidden(self):
        with pytest.raises(ValidationError):
            Environment(name="prod", unknown="x")
