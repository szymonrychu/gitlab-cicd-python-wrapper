import pytest
from pydantic import ValidationError

from gitlab_cicd_python_wrapper.variables import Variable


class TestVariable:
    def test_minimal(self):
        v = Variable(value="hello")
        assert v.value == "hello"
        assert v.description is None
        assert v.options is None
        assert v.expand is None

    def test_full(self):
        v = Variable(value="prod", description="Environment", options=["prod", "staging"], expand=False)
        assert v.description == "Environment"
        assert v.options == ["prod", "staging"]
        assert v.expand is False

    def test_extra_forbidden(self):
        with pytest.raises(ValidationError):
            Variable(value="x", unknown="y")
