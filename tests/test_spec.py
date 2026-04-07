from __future__ import annotations

import pytest
from pydantic import ValidationError

from gitlab_cicd_python_wrapper.common import InputType
from gitlab_cicd_python_wrapper.spec import ComponentInput, ComponentSpec, InputRule


class TestInputRule:
    def test_basic(self):
        r = InputRule(**{"if": "$CI_COMMIT_BRANCH == 'main'"})
        assert r.if_ == "$CI_COMMIT_BRANCH == 'main'"

    def test_with_options_and_default(self):
        r = InputRule(**{"if": "$CI"}, options=["a", "b"], default="a")
        assert r.options == ["a", "b"]
        assert r.default == "a"

    def test_alias_serialization(self):
        r = InputRule(**{"if": "$CI"})
        data = r.model_dump(by_alias=True, exclude_none=True)
        assert "if" in data
        assert "if_" not in data


class TestComponentInput:
    def test_defaults(self):
        ci = ComponentInput()
        assert ci.type == InputType.string
        assert ci.default is None

    def test_with_options(self):
        ci = ComponentInput(options=["a", "b", "c"], default="b")
        assert ci.options == ["a", "b", "c"]

    def test_default_not_in_options(self):
        with pytest.raises(ValidationError, match="must be one of options"):
            ComponentInput(options=["a", "b"], default="c")

    def test_regex_only_for_string(self):
        with pytest.raises(ValidationError, match="regex is only valid for type 'string'"):
            ComponentInput(type=InputType.number, regex="^\\d+$")

    def test_regex_valid_for_string(self):
        ci = ComponentInput(type=InputType.string, regex="^\\d+$")
        assert ci.regex == "^\\d+$"

    def test_full(self):
        ci = ComponentInput(
            type=InputType.string,
            default="hello",
            description="A greeting",
            options=["hello", "hi"],
            regex="^h",
        )
        assert ci.description == "A greeting"

    def test_number_type(self):
        ci = ComponentInput(type=InputType.number, default=42)
        assert ci.default == 42

    def test_boolean_type(self):
        ci = ComponentInput(type=InputType.boolean, default=True)
        assert ci.default is True

    def test_with_rules(self):
        ci = ComponentInput(rules=[InputRule(**{"if": "$CI"}, default="x")])
        assert len(ci.rules) == 1

    def test_extra_forbid(self):
        with pytest.raises(ValidationError):
            ComponentInput(bad="x")


class TestComponentSpec:
    def test_minimal(self):
        cs = ComponentSpec(description="My component")
        assert cs.description == "My component"

    def test_with_inputs(self):
        cs = ComponentSpec(inputs={"env": ComponentInput(default="prod")})
        assert cs.inputs["env"].default == "prod"

    def test_empty_inputs_raises(self):
        with pytest.raises(ValidationError, match="spec:inputs cannot be empty"):
            ComponentSpec(inputs={})

    def test_none_inputs_ok(self):
        cs = ComponentSpec(inputs=None)
        assert cs.inputs is None

    def test_with_include(self):
        cs = ComponentSpec(include=[{"local": "/tpl.yml"}])
        assert len(cs.include) == 1

    def test_with_component(self):
        cs = ComponentSpec(component=["comp1", "comp2"])
        assert cs.component == ["comp1", "comp2"]

    def test_extra_forbid(self):
        with pytest.raises(ValidationError):
            ComponentSpec(bad="x")
