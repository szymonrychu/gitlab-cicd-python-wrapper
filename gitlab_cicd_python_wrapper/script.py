from __future__ import annotations

from typing import Union

from pydantic import BaseModel, ConfigDict

# A single command, or a list of commands. Nested lists appear when YAML anchors/!reference are spliced in.
Script = Union[str, list[Union[str, list[str]]]]


class Hooks(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    pre_get_sources_script: Script | None = None
