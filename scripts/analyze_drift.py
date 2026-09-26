#!/usr/bin/env python3
"""Analyze pipeline drift between GitLab CI docs and the wrapper models."""

import hashlib
import logging
import os
import sys
import urllib.request
from pathlib import Path
from typing import Literal

import anthropic
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPT_FILE = REPO_ROOT / "scripts" / "analyze-pipeline-drift.md"
SOURCE_DIR = REPO_ROOT / "gitlab_cicd_python_wrapper"
README_FILE = REPO_ROOT / "README.md"

# Raw sources of https://docs.gitlab.com/ci/yaml/ and the official CI JSON schema, straight from GitLab master.
GITLAB_RAW = "https://gitlab.com/gitlab-org/gitlab/-/raw/master"
GITLAB_DOCS_URLS = [
    f"{GITLAB_RAW}/doc/ci/yaml/_index.md",
    f"{GITLAB_RAW}/doc/ci/yaml/artifacts_reports.md",
    f"{GITLAB_RAW}/doc/ci/environments/_index.md",
    f"{GITLAB_RAW}/app/assets/javascripts/editor/schema/ci.json",
]

MODEL = "claude-opus-5"
MAX_TOKENS = 16000


class DriftItem(BaseModel):
    keyword: str
    description: str
    doc_url: str
    severity: Literal["high", "medium", "low"]


class DriftReport(BaseModel):
    drift_found: bool
    items: list[DriftItem]
    summary: str


def collect_source_files() -> str:
    parts = []
    for py_file in sorted(SOURCE_DIR.rglob("*.py")):
        rel = py_file.relative_to(REPO_ROOT)
        content = py_file.read_text(encoding="utf-8")
        parts.append(f"### {rel}\n```python\n{content}\n```")
    return "\n\n".join(parts)


def fetch_docs() -> str:
    parts = []
    for url in GITLAB_DOCS_URLS:
        logger.info("Fetching %s", url)
        req = urllib.request.Request(url, headers={"User-Agent": "gitlab-cicd-python-wrapper/drift-analyzer"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            parts.append(f"### {url}\n{resp.read().decode('utf-8', errors='replace')}")
    return "\n\n".join(parts)


def read_readme() -> str:
    if README_FILE.exists():
        return README_FILE.read_text(encoding="utf-8")
    return ""


def analyze(prompt: str) -> DriftReport:
    client = anthropic.Anthropic()
    response = client.beta.messages.parse(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        # Re-run on Anthropic's recommended model if a safety classifier declines the request.
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        messages=[{"role": "user", "content": prompt}],
        output_format=DriftReport,
    )
    if response.stop_reason == "refusal":
        raise RuntimeError(f"Request refused: {response.stop_details}")
    if response.stop_reason == "max_tokens":
        raise RuntimeError(f"Response truncated at max_tokens={MAX_TOKENS}")
    return response.parsed_output


def write_report(result: DriftReport, prompt_hash: str) -> None:
    report_lines = [
        "# Pipeline Drift Report",
        "",
        f"**Summary:** {result.summary}",
        f"**Prompt hash:** `{prompt_hash}`",
        "",
        "## Drift Items",
        "",
    ]
    for item in result.items:
        report_lines.extend(
            [
                f"### `{item.keyword}` ({item.severity})",
                "",
                item.description,
                "",
                f"Documentation: {item.doc_url}",
                "",
            ]
        )

    report_path = REPO_ROOT / "drift-report.md"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    logger.info("Drift report written to %s", report_path)

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write("drift_detected=true\n")


def main() -> int:
    prompt_template = PROMPT_FILE.read_text(encoding="utf-8")
    prompt = prompt_template.replace("{source_code}", collect_source_files())
    prompt = prompt.replace("{docs_content}", fetch_docs())
    prompt = prompt.replace("{readme_content}", read_readme())

    prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]
    logger.info("Prompt hash: %s", prompt_hash)

    logger.info("Calling Anthropic API (%s)...", MODEL)
    result = analyze(prompt)
    logger.info("Drift found: %s", result.drift_found)

    if result.drift_found and result.items:
        write_report(result, prompt_hash)
    else:
        logger.info("No drift detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
