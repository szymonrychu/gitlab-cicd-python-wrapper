from gitlab_cicd_python_wrapper.artifacts import Artifacts
from gitlab_cicd_python_wrapper.cache import Cache
from gitlab_cicd_python_wrapper.common import WhenCondition
from gitlab_cicd_python_wrapper.image import Image, Service
from gitlab_cicd_python_wrapper.job import AllowFailure, Inherit, Job, Parallel
from gitlab_cicd_python_wrapper.needs import Need
from gitlab_cicd_python_wrapper.rules import Rule
from gitlab_cicd_python_wrapper.trigger import Trigger


def test_job_minimal():
    j = Job(script=["echo hello"])
    assert j.script == ["echo hello"]
    assert j.stage is None


def test_job_with_stage():
    j = Job(script=["make build"], stage="build")
    assert j.stage == "build"


def test_job_with_image_string():
    j = Job(script=["test"], image="python:3.11")
    assert j.image == "python:3.11"


def test_job_with_image_object():
    j = Job(script=["test"], image=Image(name="python:3.11", entrypoint=["/bin/sh"]))
    assert j.image.name == "python:3.11"


def test_job_with_rules():
    j = Job(
        script=["deploy"],
        rules=[Rule(if_='$CI_COMMIT_BRANCH == "main"', when=WhenCondition.always)],
    )
    assert len(j.rules) == 1


def test_job_with_artifacts():
    j = Job(script=["build"], artifacts=Artifacts(paths=["dist/"]))
    assert j.artifacts.paths == ["dist/"]


def test_job_with_cache_list():
    j = Job(
        script=["build"],
        cache=[Cache(paths=["node_modules/"], key="npm"), Cache(paths=[".pip/"], key="pip")],
    )
    assert len(j.cache) == 2


def test_job_with_needs():
    j = Job(script=["test"], needs=["build", Need(job="lint", artifacts=False)])
    assert len(j.needs) == 2


def test_job_with_services():
    j = Job(
        script=["test"],
        services=["postgres:15", Service(name="redis:7", alias="cache")],
    )
    assert len(j.services) == 2


def test_job_allow_failure_bool():
    j = Job(script=["test"], allow_failure=True)
    assert j.allow_failure is True


def test_job_allow_failure_exit_codes():
    j = Job(script=["test"], allow_failure=AllowFailure(exit_codes=[137, 143]))
    assert j.allow_failure.exit_codes == [137, 143]


def test_job_parallel_int():
    j = Job(script=["test"], parallel=5)
    assert j.parallel == 5


def test_job_parallel_matrix():
    j = Job(
        script=["test"],
        parallel=Parallel(matrix=[{"PYTHON": ["3.11", "3.12"], "DB": ["postgres", "mysql"]}]),
    )
    assert len(j.parallel.matrix) == 1


def test_job_extends_string():
    j = Job(script=["test"], extends=".base-job")
    assert j.extends == ".base-job"


def test_job_extends_list():
    j = Job(script=["test"], extends=[".base-job", ".deploy-job"])
    assert j.extends == [".base-job", ".deploy-job"]


def test_job_trigger():
    j = Job(trigger=Trigger(project="org/downstream"))
    assert j.trigger.project == "org/downstream"
    assert j.script is None


def test_job_when():
    j = Job(script=["test"], when=WhenCondition.manual)
    assert j.when == WhenCondition.manual


def test_job_inherit():
    j = Job(script=["test"], inherit=Inherit(default=False, variables=["VAR1"]))
    assert j.inherit.default is False
    assert j.inherit.variables == ["VAR1"]


def test_job_environment_string():
    j = Job(script=["deploy"], environment="production")
    assert j.environment == "production"


def test_job_timeout():
    j = Job(script=["test"], timeout="1 hour")
    assert j.timeout == "1 hour"
