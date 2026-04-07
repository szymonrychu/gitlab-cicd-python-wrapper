from __future__ import annotations

import pytest
from pydantic import ValidationError

from gitlab_cicd_python_wrapper.include import (
    ComponentReference,
    IncludeComponent,
    IncludeLocal,
    IncludeProject,
    IncludeRemote,
    IncludeTemplate,
)


class TestComponentReference:
    def test_from_string(self):
        ref = ComponentReference.from_string("gitlab.example.com/my-org/my-project/my-component@1.0.0")
        assert ref.fqdn == "gitlab.example.com"
        assert ref.project_path == "my-org/my-project"
        assert ref.component_name == "my-component"
        assert ref.version == "1.0.0"

    def test_from_string_nested(self):
        ref = ComponentReference.from_string("gitlab.com/a/b/c/d/comp@main")
        assert ref.fqdn == "gitlab.com"
        assert ref.project_path == "a/b/c/d"
        assert ref.component_name == "comp"
        assert ref.version == "main"


class TestIncludeLocal:
    def test_basic(self):
        i = IncludeLocal(local="/templates/.gitlab-ci-template.yml")
        assert i.local == "/templates/.gitlab-ci-template.yml"

    def test_with_inputs(self):
        i = IncludeLocal(local="/tpl.yml", inputs={"env": "prod"})
        assert i.inputs["env"] == "prod"

    def test_with_rules(self):
        i = IncludeLocal(local="/tpl.yml", rules=[{"if": "$CI"}])
        assert len(i.rules) == 1

    def test_extra_forbid(self):
        with pytest.raises(ValidationError):
            IncludeLocal(local="/x.yml", bad="y")


class TestIncludeRemote:
    def test_basic(self):
        i = IncludeRemote(remote="https://example.com/ci.yml")
        assert i.remote == "https://example.com/ci.yml"

    def test_with_integrity(self):
        i = IncludeRemote(remote="https://example.com/ci.yml", integrity="sha256-abc")
        assert i.integrity == "sha256-abc"

    def test_with_cache(self):
        i = IncludeRemote(remote="https://example.com/ci.yml", cache=True)
        assert i.cache is True


class TestIncludeTemplate:
    def test_basic(self):
        i = IncludeTemplate(template="Auto-DevOps.gitlab-ci.yml")
        assert i.template == "Auto-DevOps.gitlab-ci.yml"

    def test_with_inputs(self):
        i = IncludeTemplate(template="tpl.yml", inputs={"key": "val"})
        assert i.inputs["key"] == "val"


class TestIncludeProject:
    def test_basic(self):
        i = IncludeProject(project="my-group/my-project", file="/templates/ci.yml")
        assert i.project == "my-group/my-project"
        assert i.file == "/templates/ci.yml"

    def test_file_list(self):
        i = IncludeProject(project="p", file=["/a.yml", "/b.yml"])
        assert len(i.file) == 2

    def test_with_ref(self):
        i = IncludeProject(project="p", file="/a.yml", ref="main")
        assert i.ref == "main"


class TestIncludeComponent:
    def test_basic(self):
        i = IncludeComponent(component="gitlab.com/org/proj/comp@1.0")
        assert i.component == "gitlab.com/org/proj/comp@1.0"

    def test_parsed_ref(self):
        i = IncludeComponent(component="gitlab.com/org/proj/comp@1.0")
        ref = i.parsed_ref
        assert ref.fqdn == "gitlab.com"
        assert ref.project_path == "org/proj"
        assert ref.component_name == "comp"
        assert ref.version == "1.0"

    def test_with_inputs(self):
        i = IncludeComponent(component="gitlab.com/o/p/c@v1", inputs={"x": "y"})
        assert i.inputs["x"] == "y"
