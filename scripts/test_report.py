#!/usr/bin/env python3
"""Run a test command and write an auditable Markdown report."""

import argparse
import datetime as dt
import hashlib
import subprocess
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--test", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
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
    content = f"""# Test Report: `{args.source.name}`

## Result

| Field | Value |
|---|---|
| Status | **{status}** |
| Exit code | `{result.returncode}` |
| Run at | `{timestamp}` |
| Source SHA-256 | `{digest(args.source)}` |
| Test SHA-256 | `{digest(args.test)}` |

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
