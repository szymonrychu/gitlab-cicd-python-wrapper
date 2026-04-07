import pytest
from pydantic import ValidationError

from gitlab_cicd_python_wrapper.image import Image, Service


class TestImage:
    def test_minimal(self):
        img = Image(name="python:3.11")
        assert img.name == "python:3.11"
        assert img.entrypoint is None
        assert img.pull_policy is None

    def test_full(self):
        img = Image(name="python:3.11", entrypoint=["/bin/sh", "-c"], pull_policy="always")
        assert img.entrypoint == ["/bin/sh", "-c"]
        assert img.pull_policy == "always"

    def test_entrypoint_string(self):
        img = Image(name="python:3.11", entrypoint="/bin/sh")
        assert img.entrypoint == "/bin/sh"

    def test_extra_forbidden(self):
        with pytest.raises(ValidationError):
            Image(name="python:3.11", foo="bar")


class TestService:
    def test_minimal(self):
        svc = Service(name="postgres:15")
        assert svc.name == "postgres:15"
        assert svc.alias is None

    def test_full(self):
        svc = Service(
            name="postgres:15",
            alias="db",
            entrypoint=["/bin/sh"],
            command=["--max-connections=100"],
            pull_policy="if-not-present",
            variables={"POSTGRES_DB": "test"},
        )
        assert svc.alias == "db"
        assert svc.variables == {"POSTGRES_DB": "test"}

    def test_extra_forbidden(self):
        with pytest.raises(ValidationError):
            Service(name="postgres:15", unknown="x")
