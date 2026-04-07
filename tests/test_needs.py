import pytest
from pydantic import ValidationError

from gitlab_cicd_python_wrapper.needs import Need, NeedsPipeline


class TestNeed:
    def test_minimal(self):
        n = Need(job="build")
        assert n.job == "build"
        assert n.artifacts is None
        assert n.optional is None

    def test_full(self):
        n = Need(job="build", artifacts=True, optional=False)
        assert n.artifacts is True
        assert n.optional is False

    def test_extra_forbidden(self):
        with pytest.raises(ValidationError):
            Need(job="build", foo="bar")


class TestNeedsPipeline:
    def test_minimal(self):
        n = NeedsPipeline(pipeline="other/project", job="build")
        assert n.pipeline == "other/project"
        assert n.job == "build"
        assert n.artifacts is None

    def test_full(self):
        n = NeedsPipeline(pipeline="other/project", job="build", artifacts=True)
        assert n.artifacts is True

    def test_extra_forbidden(self):
        with pytest.raises(ValidationError):
            NeedsPipeline(pipeline="p", job="j", unknown="x")
