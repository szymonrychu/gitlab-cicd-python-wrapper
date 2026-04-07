from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class VaultEngine(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    name: str
    path: str


class VaultConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    engine: VaultEngine
    path: str
    field: str


class Secret(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    vault: VaultConfig
