from pathlib import Path

from gitlab_cicd_python_wrapper.serialization import (
    dump_yaml,
    load_yaml,
    yaml_round_trip,
)

FIXTURES = Path(__file__).parent / "fixtures"


class TestLoadYaml:
    def test_load_yaml_minimal(self):
        plain, raw = load_yaml(FIXTURES / "minimal.yml")
        assert "stages" in plain
        assert plain["stages"] == ["build", "test"]
        assert "build-job" in plain

    def test_load_yaml_from_string(self):
        yaml_str = "stages:\n  - build\nfoo:\n  script: echo hi\n"
        plain, raw = load_yaml(yaml_str)
        assert plain["stages"] == ["build"]
        assert "foo" in plain


class TestRoundTrip:
    def test_round_trip_preserves_comments(self):
        source = FIXTURES / "with_comments.yml"
        original = source.read_text()
        result = yaml_round_trip(source)
        assert result == original

    def test_round_trip_preserves_ordering(self):
        source = FIXTURES / "complex.yml"
        original = source.read_text()
        result = yaml_round_trip(source)
        assert result == original

    def test_round_trip_minimal(self):
        source = FIXTURES / "minimal.yml"
        original = source.read_text()
        result = yaml_round_trip(source)
        assert result == original


class TestDumpYaml:
    def test_dump_yaml_to_file(self, tmp_path):
        _, raw = load_yaml(FIXTURES / "minimal.yml")
        out = tmp_path / "output.yml"
        text = dump_yaml(raw, out)
        assert out.read_text() == text
        assert "stages" in text
