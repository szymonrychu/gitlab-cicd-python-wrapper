# Gitlab CICD Python Wrapper

Pydantic models wrapping every GitLab CI/CD YAML keyword with 1:1 mapping to
[GitLab CI/CD YAML reference](https://docs.gitlab.com/ci/yaml/).

## Features

- Programmatic pipeline generation using Python-native objects
- Validation framework for existing pipelines
- Comment-preserving round-trip serialization (load -> validate -> write = identical YAML)
- GitLab CI/CD Component parsing with input validation
- Both sync and async APIs
- CLI validator and pre-commit hook

## Installation

```bash
pip install gitlab-cicd-python-wrapper
```

Or with Poetry:

```bash
poetry add gitlab-cicd-python-wrapper
```

## Compatibility Matrix

| GitLab Version | Pipeline Coverage | Component Coverage | Notes |
|----------------|-------------------|-------------------|-------|
| 17.x           | Full              | Full              | All keywords as of 17.9 |
| 16.x           | Full              | Partial           | Components GA in 17.0 |
| 15.x           | Partial           | N/A               | Deprecated keywords still accepted |

## Quick Start

### Generate a Pipeline

```python
from gitlab_cicd_python_wrapper import Pipeline, Job, Image, Artifacts

pipeline = Pipeline(
    stages=["build", "test", "deploy"],
    jobs={
        "build": Job(
            stage="build",
            image=Image(name="python:3.11"),
            script=["pip install -r requirements.txt", "python setup.py build"],
            artifacts=Artifacts(paths=["dist/"]),
        ),
        "test": Job(
            stage="test",
            script=["pytest"],
            needs=["build"],
        ),
    },
)

print(pipeline.to_yaml())
```

### Validate an Existing Pipeline

```python
from gitlab_cicd_python_wrapper import Pipeline

# Load and validate
pipeline = Pipeline.from_yaml(".gitlab-ci.yml")
print(f"Stages: {pipeline.stages}")
print(f"Jobs: {list(pipeline.jobs.keys())}")

# Validate without loading
errors = Pipeline.validate_file(".gitlab-ci.yml")
if errors:
    for err in errors:
        print(f"Error: {err}")
```

### Round-Trip Editing (Comments Preserved)

```python
from gitlab_cicd_python_wrapper import Pipeline

# Load -> modify -> save preserves comments and formatting
pipeline = Pipeline.from_yaml(".gitlab-ci.yml")
pipeline.to_yaml("validated-output.yml")
# Output is byte-identical to input for unmodified pipelines
```

## CLI Validator

```bash
# Validate pipeline files
gitlab-cicd-validate .gitlab-ci.yml

# Validate multiple files
gitlab-cicd-validate .gitlab-ci.yml .gitlab/ci/*.yml

# Validate component templates
gitlab-cicd-validate --component templates/build.yml

# JSON output
gitlab-cicd-validate --format json .gitlab-ci.yml

# Strict mode (fail on warnings)
gitlab-cicd-validate --strict .gitlab-ci.yml
```

## Pre-commit Hook

Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/szymonrychu/gitlab-cicd-python-wrapper
    rev: v0.1.0
    hooks:
      - id: gitlab-cicd-validate
        args: ['--strict']
      - id: gitlab-cicd-validate-components
```

This validates `.gitlab-ci.yml` and any YAML files under `.gitlab/ci/` automatically,
plus component templates under `templates/`.

## Component Parsing

Parse and validate GitLab CI/CD components with input validation:

```python
from gitlab_cicd_python_wrapper import Component

# Load a component template
component = Component.from_yaml("templates/deploy.yml")

# Inspect the spec
for name, input_def in component.spec.inputs.items():
    print(f"{name}: type={input_def.type}, default={input_def.default}")

# Validate inputs (raises ValueError on failure)
resolved = component.validate_inputs({
    "stage": "deploy",
    "environment": "production",
    "timeout": 3600,
})

# Render with inputs interpolated (returns a Pipeline)
pipeline = component.render({
    "stage": "deploy",
    "environment": "production",
    "timeout": 3600,
})
print(pipeline.to_yaml())
```

## Dynamic Child Pipelines

Generate pipelines dynamically for use with `trigger:include`:

```python
from gitlab_cicd_python_wrapper import Pipeline, Job

services = ["api", "web", "worker"]

jobs = {}
for svc in services:
    jobs[f"build-{svc}"] = Job(
        stage="build",
        image="docker:latest",
        script=[f"docker build -t {svc} services/{svc}/"],
        tags=["docker"],
    )

child = Pipeline(stages=["build"], jobs=jobs)
child.to_yaml("generated-pipeline.yml")

# Parent pipeline triggers it:
# trigger:
#   include:
#     - artifact: generated-pipeline.yml
#       job: generate-pipeline
```

## Async API

```python
import asyncio
from gitlab_cicd_python_wrapper import AsyncPipeline, AsyncComponent

async def main():
    # Pipeline
    pipeline = await AsyncPipeline.from_yaml(".gitlab-ci.yml")
    print(f"Stages: {pipeline.stages}")
    print(f"Jobs: {list(pipeline.jobs.keys())}")
    await AsyncPipeline.to_yaml(pipeline, "validated-output.yml")

    # Component
    component = await AsyncComponent.from_yaml("templates/build.yml")
    resolved = component.validate_inputs({"image": "python:3.12"})

asyncio.run(main())
```

## Docker

Run the validator as a container:

```bash
docker run --rm -v $(pwd):/data szymonrychu/gitlab-cicd-python-wrapper /data/.gitlab-ci.yml
```

## PyPI Configuration

To publish this library to PyPI using GitHub Actions trusted publishing:

1. Create an account at [pypi.org](https://pypi.org)
2. Go to "Your projects" -> "Publishing" -> "Add a new pending publisher"
3. Set: GitHub owner=`szymonrychu`, repo=`gitlab-cicd-python-wrapper`,
   workflow=`pypi.yaml`, environment=`pypi`
4. Create a GitHub environment named `pypi` in your repo settings
5. Push a semantic version tag (e.g., `v0.1.0`) to trigger the publish workflow

## Development

```bash
# Install dependencies
mise install
poetry install

# Run tests
poetry run pytest

# Run linters
pre-commit run --all-files

# Run CLI
poetry run gitlab-cicd-validate .gitlab-ci.yml
```

## License

MIT
