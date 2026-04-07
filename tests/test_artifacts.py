from __future__ import annotations

import pytest
from pydantic import ValidationError

from gitlab_cicd_python_wrapper.artifacts import ArtifactReports, Artifacts
from gitlab_cicd_python_wrapper.common import ArtifactAccess, ArtifactWhen


class TestArtifactReports:
    def test_empty(self):
        r = ArtifactReports()
        assert r.junit is None

    def test_junit_string(self):
        r = ArtifactReports(junit="report.xml")
        assert r.junit == "report.xml"

    def test_junit_list(self):
        r = ArtifactReports(junit=["a.xml", "b.xml"])
        assert r.junit == ["a.xml", "b.xml"]

    def test_coverage_report(self):
        r = ArtifactReports(coverage_report={"coverage_format": "cobertura", "path": "cov.xml"})
        assert r.coverage_report["path"] == "cov.xml"

    def test_extra_allowed(self):
        r = ArtifactReports(custom_report="foo.json")
        assert r.model_extra["custom_report"] == "foo.json"

    def test_all_report_types(self):
        r = ArtifactReports(
            codequality="gl-code-quality-report.json",
            sast="gl-sast-report.json",
            dependency_scanning="dep.json",
            container_scanning="cs.json",
            dast="dast.json",
            license_scanning="ls.json",
            performance="perf.json",
            dotenv="build.env",
            terraform="tfplan.json",
            metrics="metrics.txt",
            requirements="req.json",
            secret_detection="sd.json",
            cyclonedx="sbom.json",
        )
        assert r.codequality == "gl-code-quality-report.json"
        assert r.cyclonedx == "sbom.json"


class TestArtifacts:
    def test_minimal(self):
        a = Artifacts(paths=["build/"])
        assert a.paths == ["build/"]
        assert a.expire_in is None

    def test_full(self):
        a = Artifacts(
            paths=["build/"],
            exclude=["build/tmp"],
            expire_in="1 week",
            expose_as="Build output",
            name="my-artifact",
            public=True,
            access=ArtifactAccess.developer,
            untracked=False,
            when=ArtifactWhen.on_success,
            reports=ArtifactReports(junit="report.xml"),
        )
        assert a.access == ArtifactAccess.developer
        assert a.when == ArtifactWhen.on_success
        assert a.reports.junit == "report.xml"

    def test_extra_forbid(self):
        with pytest.raises(ValidationError):
            Artifacts(paths=["x"], bogus="y")

    def test_serialization_roundtrip(self):
        a = Artifacts(paths=["dist/"], when=ArtifactWhen.always)
        data = a.model_dump(exclude_none=True)
        a2 = Artifacts(**data)
        assert a2 == a
