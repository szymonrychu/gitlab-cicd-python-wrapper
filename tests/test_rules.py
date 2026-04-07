from __future__ import annotations

import pytest
from pydantic import ValidationError

from gitlab_cicd_python_wrapper.common import WhenCondition
from gitlab_cicd_python_wrapper.rules import Rule, WorkflowRule


class TestRule:
    def test_if_alias(self):
        r = Rule(**{"if": "$CI_PIPELINE_SOURCE == 'merge_request_event'"})
        assert r.if_ == "$CI_PIPELINE_SOURCE == 'merge_request_event'"

    def test_if_field_name(self):
        r = Rule(if_="$VAR == 'x'")
        assert r.if_ == "$VAR == 'x'"

    def test_changes(self):
        r = Rule(changes=["src/**/*"])
        assert r.changes == ["src/**/*"]

    def test_full(self):
        r = Rule(
            **{"if": "$CI"},
            changes=["*.py"],
            exists=["Dockerfile"],
            when=WhenCondition.manual,
            allow_failure=True,
            variables={"DEPLOY": "true"},
            start_in="5 minutes",
        )
        assert r.when == WhenCondition.manual
        assert r.allow_failure is True
        assert r.start_in == "5 minutes"

    def test_extra_forbid(self):
        with pytest.raises(ValidationError):
            Rule(bad="x")

    def test_serialization_by_alias(self):
        r = Rule(**{"if": "$VAR"})
        data = r.model_dump(by_alias=True, exclude_none=True)
        assert "if" in data
        assert "if_" not in data


class TestWorkflowRule:
    def test_basic(self):
        wr = WorkflowRule(**{"if": "$CI_COMMIT_BRANCH"})
        assert wr.if_ == "$CI_COMMIT_BRANCH"

    def test_auto_cancel(self):
        wr = WorkflowRule(
            **{"if": "$CI"},
            auto_cancel={"on_new_commit": "interruptible"},
        )
        assert wr.auto_cancel["on_new_commit"] == "interruptible"

    def test_extra_forbid(self):
        with pytest.raises(ValidationError):
            WorkflowRule(nope="x")
