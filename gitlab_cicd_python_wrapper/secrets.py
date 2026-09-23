from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator


class VaultEngine(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    name: str
    path: str


class VaultConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    engine: VaultEngine
    path: str
    field: str


class GcpSecretManager(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    name: str
    version: str | int | None = None


class AzureKeyVault(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    name: str
    version: str | None = None


class AwsSecretsManager(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    secret_id: str
    version_id: str | None = None
    version_stage: str | None = None
    region: str | None = None
    role_arn: str | None = None
    role_session_name: str | None = None
    field: str | None = None


class GitlabSecretsManager(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    name: str = Field(pattern=r"^[a-zA-Z0-9_]+$")
    source: str | None = None


_PROVIDERS = ("vault", "gcp_secret_manager", "azure_key_vault", "aws_secrets_manager", "gitlab_secrets_manager")


class Secret(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    vault: str | VaultConfig | None = None
    gcp_secret_manager: GcpSecretManager | None = None
    azure_key_vault: AzureKeyVault | None = None
    aws_secrets_manager: str | AwsSecretsManager | None = None
    gitlab_secrets_manager: GitlabSecretsManager | None = None
    file: bool | None = None
    token: str | None = None

    @model_validator(mode="after")
    def exactly_one_provider(self) -> Secret:
        configured = [p for p in _PROVIDERS if getattr(self, p) is not None]
        if len(configured) != 1:
            raise ValueError(f"secret must define exactly one of {', '.join(_PROVIDERS)}; got {configured or 'none'}")
        if self.gcp_secret_manager is not None and self.token is None:
            raise ValueError("secrets:gcp_secret_manager requires secrets:token")
        return self


class IdToken(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    aud: str | list[str]
