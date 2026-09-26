from pathlib import Path

import pytest
from pydantic import ValidationError

from gitlab_cicd_python_wrapper import (
    EnvironmentAction,
    IdentityProvider,
    Job,
    JobInput,
    NeedsProject,
    Pipeline,
    RetryWhen,
    Rule,
    RuleChanges,
    RuleExists,
    Secret,
    Step,
    Trigger,
    WorkflowRule,
)

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="module")
def pipeline() -> Pipeline:
    return Pipeline.from_yaml(FIXTURES / "modern.yml")


class TestModernFixture:
    def test_globals(self, pipeline):
        assert pipeline.include == "templates/common.yml"
        assert pipeline.image == "ruby:3.3"
        assert pipeline.variables["RETRIES"] == 3
        assert pipeline.variables["DEBUG"] is False
        assert pipeline.default.identity == IdentityProvider.google_cloud
        assert pipeline.default.retry.when == RetryWhen.runner_interrupted
        assert pipeline.default.id_tokens["VAULT_ID_TOKEN"].aud[0] == "https://vault.example.com"
        assert set(pipeline.jobs) == {
            "build",
            "test",
            "deploy",
            "stop-production",
            "downstream",
            "pages",
            "legacy",
            "steps-job",
        }

    def test_job_keywords(self, pipeline):
        build = pipeline.jobs["build"]
        assert build.script == "make build"
        assert build.image.docker.platform == "arm64/v8"
        assert build.image.kubernetes.user == 1001
        assert build.parallel.matrix[1]["VERSION"] == 2
        assert build.artifacts.reports.coverage_report.path == "coverage.xml"

        test = pipeline.jobs["test"]
        assert test.inputs["workers"].default == 4
        assert isinstance(test.needs[1], NeedsProject)
        assert test.rules[0].exists.project == "group/configs"
        assert test.rules[1].changes.regexp == r"\.py$"

        deploy = pipeline.jobs["deploy"]
        assert deploy.environment.on_stop == "stop-production"
        assert deploy.environment.action == EnvironmentAction.verify
        assert deploy.environment.kubernetes.managed_resources.enabled is False
        assert deploy.release.assets.links[0].link_type == "package"
        assert deploy.secrets["DB_PASSWORD"].gitlab_secrets_manager.source == "group/platform"

        assert pipeline.jobs["downstream"].trigger.inputs == {"environment": "production"}
        assert pipeline.jobs["pages"].pages.path_prefix == "$CI_COMMIT_BRANCH"
        assert pipeline.jobs["legacy"].except_ == ["tags"]
        assert pipeline.jobs["steps-job"].run[1].inputs == {"echo": "bye"}

    def test_round_trip(self):
        source = (FIXTURES / "modern.yml").read_text()
        assert Pipeline.from_yaml(FIXTURES / "modern.yml").to_yaml() == source

    def test_generated_yaml_revalidates(self, pipeline):
        regenerated = Pipeline.model_validate(pipeline.model_dump(by_alias=True, exclude_none=True))
        regenerated._raw = None
        assert Pipeline.from_yaml(regenerated.to_yaml()).jobs.keys() == pipeline.jobs.keys()


class TestJobInputs:
    def test_default_required(self):
        with pytest.raises(ValidationError):
            JobInput()

    def test_default_type_mismatch(self):
        with pytest.raises(ValidationError):
            JobInput(type="number", default="five")
        with pytest.raises(ValidationError):
            JobInput(type="number", default=True)

    def test_default_in_options(self):
        with pytest.raises(ValidationError):
            JobInput(default="x", options=["a", "b"])


class TestRulesSyntax:
    def test_changes_requires_paths_or_regexp(self):
        with pytest.raises(ValidationError):
            RuleChanges(compare_to="main")
        with pytest.raises(ValidationError):
            RuleChanges(paths=["a"], regexp="b")

    def test_exists_ref_requires_project(self):
        with pytest.raises(ValidationError):
            RuleExists(paths=["a"], ref="main")

    def test_rule_needs_and_interruptible(self):
        r = Rule(**{"if": "$CI"}, needs=["a", {"job": "b", "optional": True}], interruptible=False)
        assert r.needs[1].optional is True

    def test_workflow_when_restricted(self):
        with pytest.raises(ValidationError):
            WorkflowRule(when="manual")


class TestRunSteps:
    def test_script_or_step(self):
        with pytest.raises(ValidationError):
            Step(name="x")
        with pytest.raises(ValidationError):
            Step(name="x", script="a", step="b")

    def test_run_excludes_script(self):
        with pytest.raises(ValidationError):
            Job(script="a", run=[Step(name="x", script="b")])


class TestSecrets:
    def test_exactly_one_provider(self):
        with pytest.raises(ValidationError):
            Secret(file=True)
        with pytest.raises(ValidationError):
            Secret(vault="a/b@c", azure_key_vault={"name": "x"})

    def test_gcp_requires_token(self):
        with pytest.raises(ValidationError):
            Secret(gcp_secret_manager={"name": "x"})

    def test_vault_short_form(self):
        assert Secret(vault="production/db/password@ops").vault == "production/db/password@ops"


class TestMisc:
    def test_identity_enum(self):
        with pytest.raises(ValidationError):
            Job(script="a", identity={"aud": "x"})

    def test_retry_int_bounds(self):
        Job(script="a", retry=2)
        with pytest.raises(ValidationError):
            Job(script="a", retry=3)

    def test_job_variables_reject_global_only_keys(self):
        with pytest.raises(ValidationError):
            Job(script="a", variables={"X": {"value": "1", "description": "nope"}})

    def test_trigger_project_and_include_exclusive(self):
        with pytest.raises(ValidationError):
            Trigger(project="a/b", include="child.yml")

    def test_pages_bool(self):
        assert Job(script="a", pages=True).pages is True
