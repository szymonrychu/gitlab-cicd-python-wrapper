from gitlab_cicd_python_wrapper.common import (
    AutoCancelOnJobFailure,
    AutoCancelOnNewCommit,
    WhenCondition,
)
from gitlab_cicd_python_wrapper.globals import AutoCancel, Default, Workflow


class TestDefault:
    def test_with_image_and_tags(self):
        d = Default(image="python:3.11", tags=["docker", "linux"])
        assert d.image == "python:3.11"
        assert d.tags == ["docker", "linux"]


class TestWorkflow:
    def test_with_name(self):
        w = Workflow(name="My Pipeline")
        assert w.name == "My Pipeline"
        assert w.rules is None

    def test_with_rules(self):
        w = Workflow(
            rules=[
                {"if": '$CI_COMMIT_BRANCH == "main"', "when": "always"},
                {"if": "$CI_MERGE_REQUEST_IID", "when": "always"},
            ]
        )
        assert len(w.rules) == 2
        assert w.rules[0].if_ == '$CI_COMMIT_BRANCH == "main"'
        assert w.rules[0].when == WhenCondition.always

    def test_auto_cancel(self):
        w = Workflow(
            auto_cancel=AutoCancel(
                on_new_commit=AutoCancelOnNewCommit.interruptible,
                on_job_failure=AutoCancelOnJobFailure.none,
            )
        )
        assert w.auto_cancel.on_new_commit == AutoCancelOnNewCommit.interruptible
        assert w.auto_cancel.on_job_failure == AutoCancelOnJobFailure.none
