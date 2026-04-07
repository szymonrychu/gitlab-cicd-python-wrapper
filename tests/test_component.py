from __future__ import annotations

from pathlib import Path

import pytest

from gitlab_cicd_python_wrapper.component import Component

FIXTURES = Path(__file__).parent / "fixtures" / "components"


class TestComponentFromYaml:
    def test_component_from_yaml(self):
        comp = Component.from_yaml(FIXTURES / "simple.yml")
        assert "stage" in comp.spec.inputs
        assert "component-job" in comp.jobs

    def test_component_multi_input(self):
        comp = Component.from_yaml(FIXTURES / "multi_input.yml")
        assert len(comp.spec.inputs) == 5
        assert comp.spec.inputs["stage"].default == "build"
        assert comp.spec.inputs["image"].default is None
        assert comp.spec.inputs["timeout"].default == 3600
        assert comp.spec.inputs["verbose"].default is False
        assert comp.spec.inputs["tags"].default == ["docker"]


class TestValidateInputs:
    def test_component_validate_inputs_defaults(self):
        comp = Component.from_yaml(FIXTURES / "simple.yml")
        resolved = comp.validate_inputs({})
        assert resolved["stage"] == "test"

    def test_component_validate_inputs_override(self):
        comp = Component.from_yaml(FIXTURES / "simple.yml")
        resolved = comp.validate_inputs({"stage": "build"})
        assert resolved["stage"] == "build"

    def test_component_validate_inputs_missing_required(self):
        comp = Component.from_yaml(FIXTURES / "multi_input.yml")
        with pytest.raises(ValueError, match="required.*image|image.*required"):
            comp.validate_inputs({})

    def test_component_validate_inputs_wrong_type(self):
        comp = Component.from_yaml(FIXTURES / "multi_input.yml")
        with pytest.raises(ValueError, match="type.*number|number.*type"):
            comp.validate_inputs({"image": "x", "timeout": "not-a-number"})

    def test_component_validate_inputs_invalid_option(self):
        comp = Component.from_yaml(FIXTURES / "invalid_inputs.yml")
        with pytest.raises(ValueError, match="must be one of"):
            comp.validate_inputs({"env": "invalid"})

    def test_component_validate_inputs_valid_option(self):
        comp = Component.from_yaml(FIXTURES / "invalid_inputs.yml")
        resolved = comp.validate_inputs({"env": "prod"})
        assert resolved["env"] == "prod"


class TestComponentToYaml:
    def test_component_to_yaml(self):
        comp = Component.from_yaml(FIXTURES / "simple.yml")
        output = comp.to_yaml()
        assert "spec:" in output
        assert "---" in output
        assert "component-job:" in output

    def test_component_round_trip(self):
        source = (FIXTURES / "simple.yml").read_text()
        comp = Component.from_yaml(FIXTURES / "simple.yml")
        output = comp.to_yaml()
        assert output == source
