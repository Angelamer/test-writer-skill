# Test Writer Skill

[![CI](https://github.com/Angelamer/test-writer-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/Angelamer/test-writer-skill/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/Angelamer/test-writer-skill/branch/main/graph/badge.svg)](https://codecov.io/gh/Angelamer/test-writer-skill)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

A provider-neutral skill and command-line workflow for designing Python tests, running quality checks, and producing evidence-based Markdown reports. It works with any coding agent and does not require an external LLM.

## What it provides

- A concise [`SKILL.md`](SKILL.md) workflow for unit and integration test generation.
- `unittest`-compatible execution with configurable source, test, and report paths.
- Black formatting, Flake8 linting, compilation checks, coverage, and aggregate QA commands.
- Markdown reports containing hashes, timestamps, target-source coverage, CI metadata, exact commands, exit codes, and raw output.
- Optional OpenAI-compatible, Ollama, or prompt-only model invocation without third-party Python SDKs.
- A tested numerical example that keeps model files and plotting outside the unit-test boundary.

## Repository layout

```text
.
├── SKILL.md                         # Instructions consumed by coding agents
├── Makefile                         # Reproducible developer and reporting commands
├── agents/openai.yaml               # Optional Codex UI metadata
├── scripts/
│   ├── invoke_model.py              # Optional model-provider adapter
│   └── test_report.py               # Test runner and Markdown report generator
├── references/model-providers.md    # Hosted and local model configuration
├── tests/test_tools.py              # Tests for the deterministic tooling
└── examples/
    ├── 2nn_estimator_id.py
    ├── tests/test_2nn_estimator_id.py
    └── reports/2nn_estimator_id-report.md
```

## Quick start

Python 3.10 or newer is recommended.

```bash
git clone https://github.com/Angelamer/test-writer-skill.git
cd test-writer-skill
python -m pip install -r requirements-dev.txt
make qa
make report-example
```

Run `make help` to list all commands. The default interpreter is `python`; override it when needed, for example `make PYTHON=python3 qa`.

## Make commands

| Command | Purpose |
|---|---|
| `make pretty` | Format Python code with Black. |
| `make pretty-check` | Verify formatting without modifying files. |
| `make lint` | Run Flake8. |
| `make compile` | Compile Python files to detect syntax errors. |
| `make validate-skill` | Validate skill metadata when the Codex validator is installed. |
| `make test` | Run tests for the bundled tools. |
| `make test-example` | Run the 2NN example tests with a non-interactive plot backend. |
| `make test-all` | Run tool and example tests. |
| `make test-cov` | Run all discovered tests and generate JSON/XML coverage. |
| `make coverage-html` | Generate `htmlcov/index.html` with annotated source lines. |
| `make report-example` | Rebuild the tracked 2NN Markdown report. |
| `make qa` | Run formatting, lint, compilation, skill validation, and all tests. |
| `make qa-fix` | Format the code and then run `make qa`. |
| `make qa-full` | Run QA, coverage, and report generation. |

Generate a report for another source/test pair:

```bash
make report \
  SOURCE=path/to/module.py \
  TEST_FILE=path/to/test_module.py \
  REPORT=path/to/report.md
```

The test command is executed without a shell. The report is written even when tests fail, and `make` preserves the failing exit code. Its target-source section lists compact covered-line ranges, missing-line ranges, and missing branch transitions. Run `make coverage-html` for an interactive line-by-line view in `htmlcov/index.html`.

## Continuous integration and coverage

The `CI` GitHub Actions workflow runs the same checks as `make qa-full` for pushes and pull requests targeting `main`. It uploads `coverage.xml` to Codecov using GitHub OIDC, so the workflow does not require a long-lived Codecov token. The tracked example report includes coverage for the target source file only, the commit SHA, and a CI run link when generated inside GitHub Actions. Coverage from tests, skill tooling, and unrelated modules is excluded from the report field.

The CI badge reflects formatting, lint, compilation, tests, coverage generation, and report generation. Codecov upload is non-blocking because external service availability must not hide the repository's own QA result. The coverage badge is populated after the repository is activated in Codecov and Codecov processes a successful workflow upload.

## Optional model backends

The active coding agent should normally create tests directly. A separate model call is optional.

Prompt-only mode requires no credentials:

```bash
make model PROVIDER=prompt PROMPT_FILE=request.txt
```

For hosted or local endpoints, configure environment variables as documented in [`references/model-providers.md`](references/model-providers.md). Never put API keys in a Make variable, command argument, source file, or report.

## Design principles

The workflow separates three responsibilities:

1. The coding agent analyzes behavior and writes tests.
2. Make commands execute deterministic formatting, linting, testing, and reporting steps.
3. Markdown reports preserve auditable evidence and source/test hashes.

Existing project conventions take precedence over the bundled defaults. Tests should isolate external files, networks, model artifacts, and plotting while exercising the real production logic.

## Inspiration

The Make-based quality workflow and separation between source code, tests, and QA reporting were inspired by the [ICAMS-MIDS Python unittests teaching repository](https://gitlab.ruhr-uni-bochum.de/icams-mids/teaching/python_unittests/-/tree/main). This project is an independent, provider-neutral implementation and does not include the teaching repository's base unittest materials.
