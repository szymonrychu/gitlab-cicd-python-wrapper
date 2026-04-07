from __future__ import annotations

from pathlib import Path

import aiofiles

from gitlab_cicd_python_wrapper.component import Component
from gitlab_cicd_python_wrapper.pipeline import Pipeline


class AsyncPipeline:
    @classmethod
    async def from_yaml(cls, source: str | Path) -> Pipeline:
        if isinstance(source, Path):
            async with aiofiles.open(source) as f:
                content = await f.read()
            return Pipeline.from_yaml(content)
        return Pipeline.from_yaml(source)

    @classmethod
    async def to_yaml(cls, pipeline: Pipeline, target: str | Path | None = None) -> str:
        result = pipeline.to_yaml()
        if target is not None:
            async with aiofiles.open(target, "w") as f:
                await f.write(result)
        return result

    @classmethod
    async def validate_file(cls, path: Path) -> list[str]:
        async with aiofiles.open(path) as f:
            content = await f.read()
        return Pipeline.validate_file_from_string(content)


class AsyncComponent:
    @classmethod
    async def from_yaml(cls, source: str | Path) -> Component:
        if isinstance(source, Path):
            async with aiofiles.open(source) as f:
                content = await f.read()
            return Component.from_yaml(content)
        return Component.from_yaml(source)

    @classmethod
    async def to_yaml(cls, component: Component, target: str | Path | None = None) -> str:
        result = component.to_yaml()
        if target is not None:
            async with aiofiles.open(target, "w") as f:
                await f.write(result)
        return result
