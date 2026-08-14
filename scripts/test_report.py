#!/usr/bin/env python3
"""Run a test command and write an auditable Markdown report."""

import argparse
import datetime as dt
import hashlib
import json
import os
import subprocess
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def compact_lines(lines):
    numbers = sorted(set(int(line) for line in lines))
    if not numbers:
        return "none"
    ranges = []
    start = previous = numbers[0]
    for number in numbers[1:]:
        if number == previous + 1:
            previous = number
            continue
        ranges.append(str(start) if start == previous else f"{start}-{previous}")
        start = previous = number
    ranges.append(str(start) if start == previous else f"{start}-{previous}")
    return ", ".join(ranges)


def coverage_details(path, source):
    unavailable = {
        "summary": "not measured",
        "covered_lines": "not measured",
        "missing_lines": "not measured",
        "missing_branches": "not measured",
    }
    if not path.is_file():
        return unavailable
    try:
        files = json.loads(path.read_text(encoding="utf-8"))["files"]
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        return {key: "invalid coverage data" for key in unavailable}

    source_resolved = source.resolve()
    match = next(
        (
            details
            for filename, details in files.items()
            if Path(filename).resolve() == source_resolved
        ),
        None,
    )
    if match is None:
        return unavailable
    try:
        summary = match["summary"]
        percent = float(summary["percent_covered"])
        covered = int(summary["covered_lines"])
        statements = int(summary["num_statements"])
        covered_lines = compact_lines(match["executed_lines"])
        missing_lines = compact_lines(match["missing_lines"])
        missing_branches = ", ".join(
            f"{source_line} -> {'exit' if destination < 0 else destination}"
            for source_line, destination in match["missing_branches"]
        )
    except (KeyError, TypeError, ValueError):
        return {key: "invalid coverage data" for key in unavailable}
    return {
        "summary": f"{percent:.1f}% ({covered}/{statements} lines)",
        "covered_lines": covered_lines,
        "missing_lines": missing_lines,
        "missing_branches": missing_branches or "none",
    }


def repository_context(environment=None):
    environment = os.environ if environment is None else environment
    server = environment.get("GITHUB_SERVER_URL")
    repository = environment.get("GITHUB_REPOSITORY")
    sha = environment.get("GITHUB_SHA")
    run_id = environment.get("GITHUB_RUN_ID")
    if server and repository:
        commit = (
            f"[{sha[:12]}]({server}/{repository}/commit/{sha})" if sha else "unknown"
        )
        ci_run = (
            f"[GitHub Actions run]({server}/{repository}/actions/runs/{run_id})"
            if run_id
            else "not available"
        )
        return commit, ci_run
    try:
        local_sha = subprocess.run(
            ["git", "rev-parse", "--short=12", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        local_sha = "unknown"
    return f"`{local_sha}`", "local run"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--test", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--coverage-json", type=Path, default=Path("coverage.json"))
    parser.add_argument("--html-coverage-url")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("a test command is required after --")
    for path in (args.source, args.test):
        if not path.is_file():
            parser.error(f"file not found: {path}")

    result = subprocess.run(command, capture_output=True, text=True)
    output = (result.stdout + result.stderr).strip()
    status = "PASS" if result.returncode == 0 else "FAIL"
    timestamp = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    rendered_command = " ".join(command)
    commit, ci_run = repository_context()
    coverage = coverage_details(args.coverage_json, args.source)
    html_coverage = (
        f"[Open annotated source]({args.html_coverage_url})"
        if args.html_coverage_url
        else "not published"
    )
    content = f"""# Test Report: `{args.source.name}`

## Result

| Field | Value |
|---|---|
| Status | **{status}** |
| Exit code | `{result.returncode}` |
| Run at | `{timestamp}` |
| Source SHA-256 | `{digest(args.source)}` |
| Test SHA-256 | `{digest(args.test)}` |
| Target source coverage | {coverage['summary']} |
| HTML coverage | {html_coverage} |
| Commit | {commit} |
| CI | {ci_run} |

## Target Source Coverage Details

- **Covered lines:** {coverage['covered_lines']}
- **Missing lines:** {coverage['missing_lines']}
- **Missing branches:** {coverage['missing_branches']}

## Command

```text
{rendered_command}
```

## Test output

```text
{output or '(no output)'}
```
"""
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(content, encoding="utf-8")
    print(f"Wrote {args.report} ({status})")
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
