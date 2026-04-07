import pytest
from pydantic import ValidationError

from gitlab_cicd_python_wrapper.secrets import Secret, VaultConfig, VaultEngine


class TestVaultEngine:
    def test_create(self):
        e = VaultEngine(name="kv-v2", path="secret")
        assert e.name == "kv-v2"
        assert e.path == "secret"

    def test_extra_forbidden(self):
        with pytest.raises(ValidationError):
            VaultEngine(name="kv", path="s", extra="x")


class TestVaultConfig:
    def test_create(self):
        engine = VaultEngine(name="kv-v2", path="secret")
        vc = VaultConfig(engine=engine, path="production/db", field="password")
        assert vc.engine.name == "kv-v2"
        assert vc.path == "production/db"
        assert vc.field == "password"


class TestSecret:
    def test_create(self):
        s = Secret(
            vault=VaultConfig(
                engine=VaultEngine(name="kv-v2", path="secret"),
                path="production/db",
                field="password",
            )
        )
        assert s.vault.field == "password"

    def test_extra_forbidden(self):
        with pytest.raises(ValidationError):
            Secret(
                vault=VaultConfig(
                    engine=VaultEngine(name="kv", path="s"),
                    path="p",
                    field="f",
                ),
                extra="x",
            )
