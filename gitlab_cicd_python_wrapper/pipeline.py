from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator

from gitlab_cicd_python_wrapper.globals import Default, Workflow
from gitlab_cicd_python_wrapper.job import Job
from gitlab_cicd_python_wrapper.serialization import dump_yaml, load_yaml
from gitlab_cicd_python_wrapper.spec import ComponentSpec
from gitlab_cicd_python_wrapper.variables import Variable

GLOBAL_KEYWORDS = frozenset(
    {
        "stages",
        "variables",
        "default",
        "workflow",
        "include",
        "spec",
    }
)


class Pipeline(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    stages: list[str] | None = None
    variables: dict[str, str | Variable] | None = None
    default: Default | None = None
    workflow: Workflow | None = None
    include: list[dict[str, Any] | str] | None = None
    spec: ComponentSpec | None = None
    jobs: dict[str, Job] = {}

    _raw: Any = None

    @model_validator(mode="before")
    @classmethod
    def separate_jobs_from_globals(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        if "jobs" in data:
            return data
        globals_ = {}
        jobs = {}
        for key, value in data.items():
            if key in GLOBAL_KEYWORDS:
                globals_[key] = value
            else:
                jobs[key] = value
        globals_["jobs"] = jobs
        return globals_

    @classmethod
    def from_yaml(cls, source: str | Path) -> Pipeline:
        data, raw = load_yaml(source)
        pipeline = cls.model_validate(data)
        pipeline._raw = raw
        return pipeline

    def to_yaml(self, target: str | Path | None = None) -> str:
        if self._raw is not None:
            return dump_yaml(self._raw, target)
        from ruamel.yaml.comments import CommentedMap

        raw = CommentedMap()
        if self.stages:
            raw["stages"] = self.stages
        if self.variables:
            raw["variables"] = {
                k: v if isinstance(v, str) else v.model_dump(mode="json", exclude_none=True)
                for k, v in self.variables.items()
            }
        if self.default:
            raw["default"] = self.default.model_dump(mode="json", exclude_none=True, by_alias=True)
        if self.workflow:
            raw["workflow"] = self.workflow.model_dump(mode="json", exclude_none=True, by_alias=True)
        if self.include:
            raw["include"] = self.include
        for name, job in self.jobs.items():
            raw[name] = job.model_dump(mode="json", exclude_none=True, by_alias=True)
        result = dump_yaml(raw)
        if target is not None:
            Path(target).write_text(result)
        return result

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
