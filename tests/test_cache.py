from __future__ import annotations

import pytest
from pydantic import ValidationError

from gitlab_cicd_python_wrapper.cache import Cache, CacheKey
from gitlab_cicd_python_wrapper.common import CachePolicy, CacheWhen


class TestCacheKey:
    def test_minimal(self):
        ck = CacheKey(files=["Gemfile.lock"])
        assert ck.files == ["Gemfile.lock"]

    def test_with_prefix(self):
        ck = CacheKey(prefix="$CI_JOB_NAME", files=["Gemfile.lock"])
        assert ck.prefix == "$CI_JOB_NAME"

    def test_extra_forbid(self):
        with pytest.raises(ValidationError):
            CacheKey(bad="x")


class TestCache:
    def test_string_key(self):
        c = Cache(key="my-key", paths=["vendor/"])
        assert c.key == "my-key"

    def test_object_key(self):
        c = Cache(key=CacheKey(files=["Gemfile.lock"]), paths=["vendor/"])
        assert isinstance(c.key, CacheKey)

    def test_full(self):
        c = Cache(
            paths=["node_modules/"],
            key="nm-cache",
            untracked=True,
            unprotect=False,
            when=CacheWhen.on_success,
            policy=CachePolicy.pull_push,
            fallback_keys=["fallback1"],
        )
        assert c.policy == CachePolicy.pull_push
        assert c.fallback_keys == ["fallback1"]

    def test_extra_forbid(self):
        with pytest.raises(ValidationError):
            Cache(paths=["x"], nope=True)

    def test_roundtrip(self):
        c = Cache(paths=["build/"], when=CacheWhen.always)
        data = c.model_dump(exclude_none=True)
        c2 = Cache(**data)
        assert c2 == c
