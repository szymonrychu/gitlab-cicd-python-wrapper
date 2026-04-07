from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from gitlab_cicd_python_wrapper.pipeline import Pipeline

from pydantic import BaseModel, ConfigDict

from gitlab_cicd_python_wrapper.common import InputType
from gitlab_cicd_python_wrapper.job import Job
from gitlab_cicd_python_wrapper.serialization import dump_yaml_multi, load_yaml_multi
from gitlab_cicd_python_wrapper.spec import ComponentSpec

INPUT_INTERPOLATION_RE = re.compile(r"\$\[\[\s*inputs\.(\w+)\s*\]\]")
COMPONENT_INTERPOLATION_RE = re.compile(r"\$\[\[\s*component\.(\w+)\s*\]\]")
_INTERPOLATION_RE = re.compile(r"\$\[\[.+?\]\]")


def _strip_interpolation_fields(raw_job: dict) -> dict:
    stripped = {}
    for k, v in raw_job.items():
        if isinstance(v, str) and _INTERPOLATION_RE.fullmatch(v.strip()):
            continue
        stripped[k] = v
    return stripped


def _check_type(name: str, value: Any, expected: InputType) -> None:
    type_map = {
        InputType.string: str,
        InputType.number: (int, float),
        InputType.boolean: bool,
        InputType.array: list,
    }
    expected_type = type_map[expected]
    if not isinstance(value, expected_type):
        raise ValueError(f"Input '{name}' must be of type {expected.value}, got {type(value).__name__}")


class Component(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    spec: ComponentSpec
    jobs: dict[str, Job]

    _raws: list = []
    _raw_jobs: dict[str, dict] = {}

    @classmethod
    def from_yaml(cls, source: str | Path) -> Component:
        dicts, raws = load_yaml_multi(source)
        if len(dicts) < 2:
            raise ValueError("Component must have spec: section and job definitions separated by ---")
        spec_data = dicts[0].get("spec", dicts[0])
        spec = ComponentSpec.model_validate(spec_data)
        job_data = dicts[1]
        jobs = {}
        raw_jobs = {}
        for name, raw_job in job_data.items():
            raw_jobs[name] = dict(raw_job) if hasattr(raw_job, "items") else raw_job
            try:
                jobs[name] = Job.model_validate(raw_job)
            except Exception:
                jobs[name] = Job.model_validate(_strip_interpolation_fields(raw_job))
        component = cls(spec=spec, jobs=jobs)
        component._raws = raws
        component._raw_jobs = raw_jobs
        return component

    def validate_inputs(self, provided: dict[str, Any]) -> dict[str, Any]:
        if self.spec.inputs is None:
            if provided:
                raise ValueError(f"Component accepts no inputs, but got: {list(provided.keys())}")
            return {}
        resolved = {}
        for name, input_def in self.spec.inputs.items():
            if name in provided:
                value = provided[name]
            elif input_def.default is not None:
                value = input_def.default
            else:
                raise ValueError(f"Input '{name}' is required (no default provided)")
            _check_type(name, value, input_def.type)
            if input_def.options is not None and value not in input_def.options:
                raise ValueError(f"Input '{name}' value '{value}' must be one of: {input_def.options}")
            if input_def.regex is not None and isinstance(value, str):
                if not re.match(input_def.regex, value):
                    raise ValueError(f"Input '{name}' value '{value}' does not match regex: {input_def.regex}")
            resolved[name] = value
        extra = set(provided) - set(self.spec.inputs)
        if extra:
            raise ValueError(f"Unknown inputs: {extra}")
        return resolved

    def render(self, inputs: dict[str, Any]) -> "Pipeline":
        from gitlab_cicd_python_wrapper.pipeline import Pipeline

        resolved = self.validate_inputs(inputs)

        def interpolate(value: Any) -> Any:
            if isinstance(value, str):

                def replace_input(m: re.Match) -> str:
                    key = m.group(1)
                    v = resolved.get(key, m.group(0))
                    return str(v) if not isinstance(v, str) else v

                return INPUT_INTERPOLATION_RE.sub(replace_input, value)
            if isinstance(value, list):
                return [interpolate(v) for v in value]
            if isinstance(value, dict):
                return {k: interpolate(v) for k, v in value.items()}
            return value

        raw_source = (
            self._raw_jobs
            if self._raw_jobs
            else {n: j.model_dump(exclude_none=True, by_alias=True) for n, j in self.jobs.items()}
        )
        jobs = {}
        for name, raw_job in raw_source.items():
            job_data = interpolate(raw_job)
            jobs[name] = Job.model_validate(job_data)
        return Pipeline(jobs=jobs)

    def to_yaml(self, target: str | Path | None = None) -> str:
        if self._raws:
            return dump_yaml_multi(self._raws, target)
        raise NotImplementedError("to_yaml from constructed Component not yet supported")

    @classmethod
    def validate_file(cls, path: Path) -> list[str]:
        try:
            cls.from_yaml(path)
            return []
        except Exception as e:
            return [str(e)]

    @classmethod
    def validate_file_from_string(cls, content: str) -> list[str]:
        try:
            cls.from_yaml(content)
            return []
        except Exception as e:
            return [str(e)]
