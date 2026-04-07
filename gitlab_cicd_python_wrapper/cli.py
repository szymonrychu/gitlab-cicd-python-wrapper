from __future__ import annotations

import argparse
import json
from pathlib import Path

from gitlab_cicd_python_wrapper import __version__
from gitlab_cicd_python_wrapper.component import Component
from gitlab_cicd_python_wrapper.pipeline import Pipeline


def _validate_pipeline(path: Path) -> list[str]:
    return Pipeline.validate_file(path)


def _validate_component(path: Path) -> list[str]:
    return Component.validate_file(path)


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="gitlab-cicd-validate",
        description="Validate GitLab CI/CD YAML files",
    )
    parser.add_argument("files", nargs="+", type=Path, help="YAML files to validate")
    parser.add_argument("--strict", action="store_true", help="Enable strict validation")
    parser.add_argument("--component", action="store_true", help="Validate as component")
    parser.add_argument(
        "--format", choices=["text", "json"], default="text", dest="output_format", help="Output format"
    )
    parser.add_argument("--quiet", action="store_true", help="Suppress output on success")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    args = parser.parse_args()

    all_valid = True
    results: list[dict] = []

    for file_path in args.files:
        if args.component:
            errors = _validate_component(file_path)
        else:
            errors = _validate_pipeline(file_path)

        valid = len(errors) == 0
        if not valid:
            all_valid = False

        result = {"file": str(file_path), "valid": valid, "errors": errors}
        results.append(result)

    if args.output_format == "json":
        print(json.dumps(results, indent=2))
    elif not args.quiet:
        for result in results:
            if result["valid"]:
                print(f"{result['file']}: valid")
            else:
                print(f"{result['file']}: invalid")
                for error in result["errors"]:
                    print(f"  - {error}")
    elif not all_valid:
        for result in results:
            if not result["valid"]:
                print(f"{result['file']}: invalid")
                for error in result["errors"]:
                    print(f"  - {error}")

    return 0 if all_valid else 1
