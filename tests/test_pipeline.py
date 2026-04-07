from pathlib import Path

from gitlab_cicd_python_wrapper.pipeline import Pipeline

FIXTURES = Path(__file__).parent / "fixtures"


class TestPipelineFromDict:
    def test_pipeline_from_dict(self):
        p = Pipeline(
            stages=["build", "test"],
            jobs={
                "build-job": {"stage": "build", "script": ["echo build"]},
                "test-job": {"stage": "test", "script": ["echo test"]},
            },
        )
        assert p.stages == ["build", "test"]
        assert "build-job" in p.jobs
        assert "test-job" in p.jobs
        assert p.jobs["build-job"].stage == "build"


class TestPipelineFromYaml:
    def test_pipeline_from_yaml_minimal(self):
        p = Pipeline.from_yaml(FIXTURES / "minimal.yml")
        assert p.stages == ["build", "test"]
        assert "build-job" in p.jobs
        assert p.jobs["build-job"].stage == "build"

    def test_pipeline_from_yaml_complex(self):
        p = Pipeline.from_yaml(FIXTURES / "complex.yml")
        assert p.stages == ["build", "test", "deploy"]
        assert p.default is not None
        assert p.workflow is not None
        assert p.include is not None
        assert len(p.jobs) == 3
        assert "build" in p.jobs
        assert "test" in p.jobs
        assert "deploy" in p.jobs

    def test_pipeline_from_yaml_string(self):
        yaml_str = "stages:\n  - build\nmy-job:\n  stage: build\n  script:\n    - echo hi\n"
        p = Pipeline.from_yaml(yaml_str)
        assert p.stages == ["build"]
        assert "my-job" in p.jobs
        assert p.jobs["my-job"].script == ["echo hi"]


class TestPipelineToYaml:
    def test_pipeline_to_yaml(self):
        p = Pipeline(
            stages=["build"],
            jobs={"build-job": {"stage": "build", "script": ["echo build"]}},
        )
        result = p.to_yaml()
        assert "stages" in result
        assert "build-job" in result
        assert "echo build" in result

    def test_pipeline_round_trip_comments(self):
        source = FIXTURES / "with_comments.yml"
        original = source.read_text()
        p = Pipeline.from_yaml(source)
        result = p.to_yaml()
        assert result == original

    def test_pipeline_round_trip_complex(self):
        source = FIXTURES / "complex.yml"
        original = source.read_text()
        p = Pipeline.from_yaml(source)
        result = p.to_yaml()
        assert result == original

    def test_pipeline_to_yaml_file(self, tmp_path):
        p = Pipeline.from_yaml(FIXTURES / "minimal.yml")
        out = tmp_path / "output.yml"
        result = p.to_yaml(out)
        assert out.read_text() == result
        assert "stages" in result


class TestPipelineValidation:
    def test_pipeline_validate_file(self):
        errors = Pipeline.validate_file(FIXTURES / "minimal.yml")
        assert errors == []

    def test_pipeline_validate_file_invalid(self, tmp_path):
        bad = tmp_path / "bad.yml"
        bad.write_text(
            "stages:\n  - build\nbad-job:\n  stage: build\n  script:\n    - echo hi\n  unknown_keyword: oops\n"
        )
        errors = Pipeline.validate_file(bad)
        assert len(errors) > 0
