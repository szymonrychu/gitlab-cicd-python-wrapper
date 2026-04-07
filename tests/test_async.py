from __future__ import annotations

from pathlib import Path

import pytest

from gitlab_cicd_python_wrapper._async import AsyncComponent, AsyncPipeline

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.mark.asyncio
async def test_async_pipeline_from_yaml():
    pipeline = await AsyncPipeline.from_yaml(FIXTURES / "minimal.yml")
    assert pipeline.stages == ["build", "test"]


@pytest.mark.asyncio
async def test_async_pipeline_to_yaml(tmp_path: Path):
    pipeline = await AsyncPipeline.from_yaml(FIXTURES / "minimal.yml")
    out = tmp_path / "out.yml"
    result = await AsyncPipeline.to_yaml(pipeline, out)
    assert out.read_text() == result
    assert "stages:" in result


@pytest.mark.asyncio
async def test_async_pipeline_round_trip():
    original = (FIXTURES / "with_comments.yml").read_text()
    pipeline = await AsyncPipeline.from_yaml(FIXTURES / "with_comments.yml")
    result = await AsyncPipeline.to_yaml(pipeline)
    assert result == original


@pytest.mark.asyncio
async def test_async_pipeline_validate_file():
    errors = await AsyncPipeline.validate_file(FIXTURES / "minimal.yml")
    assert errors == []


@pytest.mark.asyncio
async def test_async_component_from_yaml():
    component = await AsyncComponent.from_yaml(FIXTURES / "components" / "simple.yml")
    assert "component-job" in component.jobs
    assert component.spec.inputs is not None
    assert "stage" in component.spec.inputs
