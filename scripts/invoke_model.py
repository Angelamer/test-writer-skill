#!/usr/bin/env python3
"""Invoke an optional model backend without third-party Python dependencies."""

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def post_json(url, payload, api_key=None):
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    request = Request(url, json.dumps(payload).encode(), headers, method="POST")
    with urlopen(request, timeout=120) as response:
        return json.loads(response.read().decode())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--provider",
        choices=("openai-compatible", "ollama", "prompt"),
        default="prompt",
    )
    parser.add_argument("--prompt-file", type=Path, required=True)
    args = parser.parse_args()
    prompt = args.prompt_file.read_text(encoding="utf-8")

    if args.provider == "prompt":
        print(prompt)
        return

    model = os.environ.get("TEST_WRITER_MODEL")
    if not model:
        parser.error("TEST_WRITER_MODEL is required for model calls")

    try:
        if args.provider == "openai-compatible":
            base = os.environ.get("TEST_WRITER_BASE_URL", "http://127.0.0.1:8000/v1")
            data = post_json(
                f"{base.rstrip('/')}/chat/completions",
                {"model": model, "messages": [{"role": "user", "content": prompt}]},
                os.environ.get("TEST_WRITER_API_KEY"),
            )
            print(data["choices"][0]["message"]["content"])
        else:
            base = os.environ.get("TEST_WRITER_OLLAMA_URL", "http://127.0.0.1:11434")
            data = post_json(
                f"{base.rstrip('/')}/api/chat",
                {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                },
            )
            print(data["message"]["content"])
    except (HTTPError, URLError, KeyError, json.JSONDecodeError) as exc:
        print(f"Model invocation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
