import pytest
from pydantic import ValidationError

from gitlab_cicd_python_wrapper.common import RetryWhen
from gitlab_cicd_python_wrapper.retry import Retry


class TestRetry:
    def test_minimal(self):
        r = Retry(max=2)
        assert r.max == 2
        assert r.when is None

    def test_with_when(self):
        r = Retry(max=3, when=[RetryWhen.script_failure, RetryWhen.api_failure])
        assert len(r.when) == 2

    def test_max_bounds(self):
        Retry(max=0)
        Retry(max=5)
        with pytest.raises(ValidationError):
            Retry(max=-1)
        with pytest.raises(ValidationError):
            Retry(max=6)

    def test_extra_forbidden(self):
        with pytest.raises(ValidationError):
            Retry(max=1, foo="bar")
