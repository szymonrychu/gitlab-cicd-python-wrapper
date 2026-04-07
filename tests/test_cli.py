from __future__ import annotations

import json
import sys
from pathlib import Path

from gitlab_cicd_python_wrapper.cli import main

FIXTURES = Path(__file__).parent / "fixtures"


def test_cli_validate_valid(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["gitlab-cicd-validate", str(FIXTURES / "minimal.yml")])
    assert main() == 0


def test_cli_validate_complex(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["gitlab-cicd-validate", str(FIXTURES / "complex.yml")])
    assert main() == 0


def test_cli_validate_invalid(monkeypatch, tmp_path):
    bad = tmp_path / "bad.yml"
    bad.write_text("unknown_keyword: true\n")
    monkeypatch.setattr(sys, "argv", ["gitlab-cicd-validate", str(bad)])
    assert main() == 1


def test_cli_validate_component(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        ["gitlab-cicd-validate", "--component", str(FIXTURES / "components" / "simple.yml")],
    )
    assert main() == 0


def test_cli_validate_multiple_files(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        ["gitlab-cicd-validate", str(FIXTURES / "minimal.yml"), str(FIXTURES / "complex.yml")],
    )
    assert main() == 0


def test_cli_json_format(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["gitlab-cicd-validate", "--format", "json", str(FIXTURES / "minimal.yml")],
    )
    assert main() == 0
    output = capsys.readouterr().out
    data = json.loads(output)
    assert isinstance(data, list)
    assert "valid" in data[0] or "errors" in data[0]


def test_cli_quiet_valid(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["gitlab-cicd-validate", "--quiet", str(FIXTURES / "minimal.yml")],
    )
    assert main() == 0
    assert capsys.readouterr().out == ""
