import pytest
from pydantic import ValidationError

from gitlab_cicd_python_wrapper.release import Release


class TestRelease:
    def test_minimal(self):
        r = Release(tag_name="v1.0.0", description="First release")
        assert r.tag_name == "v1.0.0"
        assert r.description == "First release"
        assert r.name is None
        assert r.ref is None
        assert r.milestones is None
        assert r.released_at is None

    def test_full(self):
        r = Release(
            tag_name="v1.0.0",
            description="First release",
            name="Release 1.0",
            ref="main",
            milestones=["m1", "m2"],
            released_at="2025-01-01T00:00:00Z",
        )
        assert r.name == "Release 1.0"
        assert r.ref == "main"
        assert r.milestones == ["m1", "m2"]
        assert r.released_at == "2025-01-01T00:00:00Z"

    def test_extra_forbidden(self):
        with pytest.raises(ValidationError):
            Release(tag_name="v1", description="d", foo="bar")
