# GitLab CI/CD Drift Analysis Prompt

You are an expert in GitLab CI/CD pipeline configuration.

Analyze the following Python source code that wraps GitLab CI/CD YAML configuration.
Compare it against the current GitLab CI/CD documentation to identify any drift — meaning
keywords, options, or features that exist in GitLab CI but are not yet modeled in the wrapper.

For each piece of drift found, provide:

- The GitLab CI keyword or feature that is missing or incomplete
- A brief description of what it does
- The documentation URL where it is described
- Severity: "high" (commonly used), "medium" (moderately used), or "low" (rarely used)

Only report keywords, options, or allowed values that are genuinely missing or incorrectly modelled. The
official CI JSON schema (`ci.json`) is included alongside the docs; treat it as the source of truth for
allowed keys and enum values. Set `drift_found` to false and return an empty `items` list when the
models are in sync.

## Source Code

{source_code}

## GitLab CI/CD Documentation

{docs_content}

## README

{readme_content}
