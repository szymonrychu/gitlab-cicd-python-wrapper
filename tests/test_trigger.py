from __future__ import annotations

import pytest
from pydantic import ValidationError

from gitlab_cicd_python_wrapper.trigger import Trigger, TriggerForward


class TestTriggerForward:
    def test_empty(self):
        tf = TriggerForward()
        assert tf.yaml_variables is None

    def test_full(self):
        tf = TriggerForward(yaml_variables=True, pipeline_variables=False, dotenv_variables=True)
        assert tf.yaml_variables is True
        assert tf.pipeline_variables is False

    def test_extra_forbid(self):
        with pytest.raises(ValidationError):
            TriggerForward(bad="x")


class TestTrigger:
    def test_project(self):
        t = Trigger(project="my-group/my-project")
        assert t.project == "my-group/my-project"

    def test_with_branch_and_strategy(self):
        t = Trigger(project="p", branch="main", strategy="depend")
        assert t.branch == "main"
        assert t.strategy == "depend"

    def test_with_include(self):
        t = Trigger(include=[{"local": "/child.yml"}])
        assert len(t.include) == 1

    def test_with_forward(self):
        t = Trigger(project="p", forward=TriggerForward(yaml_variables=True))
        assert t.forward.yaml_variables is True

    def test_extra_forbid(self):
        with pytest.raises(ValidationError):
            Trigger(project="p", nope=True)

    def test_roundtrip(self):
        t = Trigger(project="p", branch="dev")
        data = t.model_dump(exclude_none=True)
        t2 = Trigger(**data)
        assert t2 == t
