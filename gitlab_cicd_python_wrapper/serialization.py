from __future__ import annotations

from io import StringIO
from pathlib import Path

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap


def _make_yaml() -> YAML:
    yaml = YAML(typ="rt")
    yaml.preserve_quotes = True
    yaml.width = 4096
    yaml.indent(mapping=2, sequence=4, offset=2)
    return yaml


def load_yaml(source: str | Path) -> tuple[dict, CommentedMap]:
    yaml = _make_yaml()
    if isinstance(source, Path):
        with open(source) as fh:
            raw = yaml.load(fh)
    else:
        raw = yaml.load(source)
    plain = dict(raw)
    return plain, raw


def dump_yaml(raw: CommentedMap, target: str | Path | None = None) -> str:
    yaml = _make_yaml()
    buf = StringIO()
    yaml.dump(raw, buf)
    text = buf.getvalue()
    if target is not None:
        path = Path(target)
        path.write_text(text)
    return text


def yaml_round_trip(source: str | Path) -> str:
    _, raw = load_yaml(source)
    return dump_yaml(raw)


def load_yaml_multi(source: str | Path) -> tuple[list[dict], list[CommentedMap]]:
    yaml = _make_yaml()
    if isinstance(source, Path):
        with open(source) as fh:
            docs = list(yaml.load_all(fh))
    else:
        docs = list(yaml.load_all(source))
    plains = [dict(d) for d in docs]
    return plains, docs


def dump_yaml_multi(raws: list[CommentedMap], target: str | Path | None = None) -> str:
    yaml = _make_yaml()
    buf = StringIO()
    yaml.dump_all(raws, buf)
    text = buf.getvalue()
    if target is not None:
        path = Path(target)
        path.write_text(text)
    return text
