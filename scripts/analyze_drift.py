#!/usr/bin/env python3
"""Analyze pipeline drift between GitLab CI docs and the wrapper models."""

import hashlib
import json
import logging
import os
import urllib.request
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPT_FILE = REPO_ROOT / "scripts" / "analyze-pipeline-drift.md"
SOURCE_DIR = REPO_ROOT / "gitlab_cicd_python_wrapper"
README_FILE = REPO_ROOT / "README.md"

GITLAB_DOCS_URLS = [
    "https://docs.gitlab.com/ee/ci/yaml/index.html",
    "https://docs.gitlab.com/ee/ci/yaml/artifacts_reports.html",
    "https://docs.gitlab.com/ee/ci/environments/index.html",
]

ANTHROPIC_MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 4096


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
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "gitlab-cicd-python-wrapper/drift-analyzer"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                text = resp.read().decode("utf-8", errors="replace")
                # Truncate to keep prompt manageable
                parts.append(f"### {url}\n{text[:20000]}")
        except Exception:
            logger.warning("Failed to fetch %s", url, exc_info=True)
    return "\n\n".join(parts)


def read_readme() -> str:
    if README_FILE.exists():
        return README_FILE.read_text(encoding="utf-8")
    return ""


def call_anthropic(prompt: str) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY environment variable is not set")

    payload = json.dumps(
        {
            "model": ANTHROPIC_MODEL,
            "max_tokens": MAX_TOKENS,
            "messages": [{"role": "user", "content": prompt}],
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    return data["content"][0]["text"]


def parse_json_response(text: str) -> dict:
    # Try to extract JSON from markdown code blocks or raw text
    if "```json" in text:
        start = text.index("```json") + 7
        end = text.index("```", start)
        text = text[start:end].strip()
    elif "```" in text:
        start = text.index("```") + 3
        end = text.index("```", start)
        text = text[start:end].strip()
    return json.loads(text)


def main():
    prompt_template = PROMPT_FILE.read_text(encoding="utf-8")
    source_code = collect_source_files()
    docs_content = fetch_docs()
    readme_content = read_readme()

    prompt = prompt_template.replace("{source_code}", source_code)
    prompt = prompt.replace("{docs_content}", docs_content)
    prompt = prompt.replace("{readme_content}", readme_content)

    prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]
    logger.info("Prompt hash: %s", prompt_hash)

    logger.info("Calling Anthropic API (%s)...", ANTHROPIC_MODEL)
    response_text = call_anthropic(prompt)

    result = parse_json_response(response_text)
    logger.info("Drift found: %s", result.get("drift_found", False))

    if result.get("drift_found"):
        report_lines = [
            "# Pipeline Drift Report",
            "",
            f"**Summary:** {result.get('summary', 'N/A')}",
            f"**Prompt hash:** `{prompt_hash}`",
            "",
            "## Drift Items",
            "",
        ]
        for item in result.get("items", []):
            report_lines.extend(
                [
                    f"### `{item['keyword']}` ({item['severity']})",
                    "",
                    item["description"],
                    "",
                    f"Documentation: {item['doc_url']}",
                    "",
                ]
            )

        report_path = REPO_ROOT / "drift-report.md"
        report_path.write_text("\n".join(report_lines), encoding="utf-8")
        logger.info("Drift report written to %s", report_path)

        # Set GITHUB_OUTPUT if running in GitHub Actions
        github_output = os.environ.get("GITHUB_OUTPUT")
        if github_output:
            with open(github_output, "a") as f:
                f.write("drift_detected=true\n")
    else:
        logger.info("No drift detected.")


if __name__ == "__main__":
    main()
