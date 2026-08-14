PYTHON ?= python
SOURCE ?= examples/2nn_estimator_id.py
TEST_FILE ?= examples/tests/test_2nn_estimator_id.py
REPORT ?= examples/reports/2nn_estimator_id-report.md
PROVIDER ?= prompt
PROMPT_FILE ?= request.txt
MPLCONFIGDIR ?= .cache/matplotlib

PYTHON_PATHS := scripts examples tests
SKILL_VALIDATOR ?= $(HOME)/.codex/skills/.system/skill-creator/scripts/quick_validate.py

.DEFAULT_GOAL := help

.PHONY: help install-dev pretty pretty-check lint compile validate-skill \
	test test-example test-all test-cov report report-example model qa qa-fix qa-full clean

help:
	@echo "Test Writer Skill commands"
	@echo "  make install-dev       Install development and example dependencies"
	@echo "  make pretty            Format Python files with Black"
	@echo "  make pretty-check      Check formatting without changing files"
	@echo "  make lint              Run Flake8"
	@echo "  make compile           Compile Python files"
	@echo "  make validate-skill    Validate SKILL.md when the Codex validator is available"
	@echo "  make test              Run tool unit tests"
	@echo "  make test-example      Run the bundled 2NN example tests"
	@echo "  make test-all          Run tool and example tests"
	@echo "  make test-cov          Run all tests with branch coverage"
	@echo "  make report            Run TEST_FILE and write REPORT for SOURCE"
	@echo "  make report-example    Generate the bundled example report"
	@echo "  make model             Invoke PROVIDER using PROMPT_FILE"
	@echo "  make qa                Check format, lint, compile, validate, and test"
	@echo "  make qa-fix            Format, then run qa"
	@echo "  make qa-full           Run qa, coverage, and the example report"

install-dev:
	$(PYTHON) -m pip install -r requirements-dev.txt

pretty:
	$(PYTHON) -m black $(PYTHON_PATHS)

pretty-check:
	$(PYTHON) -m black --check $(PYTHON_PATHS)

lint:
	$(PYTHON) -m flake8 $(PYTHON_PATHS) --max-line-length=100

compile:
	$(PYTHON) -m compileall -q $(PYTHON_PATHS)

validate-skill:
	@if [ -f "$(SKILL_VALIDATOR)" ]; then \
		$(PYTHON) "$(SKILL_VALIDATOR)" .; \
	else \
		echo "Skill validator not found; checked SKILL.md presence only."; \
		test -f SKILL.md; \
	fi

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py' -v

test-example:
	MPLBACKEND=Agg MPLCONFIGDIR="$(MPLCONFIGDIR)" $(PYTHON) -m unittest -v $(TEST_FILE)

test-all: test test-example

test-cov:
	MPLBACKEND=Agg MPLCONFIGDIR="$(MPLCONFIGDIR)" $(PYTHON) -m coverage run --branch -m unittest -v \
		tests/test_tools.py $(TEST_FILE)
	$(PYTHON) -m coverage report -m

report:
	@test -f "$(SOURCE)" || (echo "SOURCE not found: $(SOURCE)"; exit 2)
	@test -f "$(TEST_FILE)" || (echo "TEST_FILE not found: $(TEST_FILE)"; exit 2)
	MPLBACKEND=Agg MPLCONFIGDIR="$(MPLCONFIGDIR)" $(PYTHON) scripts/test_report.py \
		--source "$(SOURCE)" \
		--test "$(TEST_FILE)" \
		--report "$(REPORT)" \
		-- $(PYTHON) -m unittest -v "$(TEST_FILE)"

report-example:
	$(MAKE) report \
		SOURCE=examples/2nn_estimator_id.py \
		TEST_FILE=examples/tests/test_2nn_estimator_id.py \
		REPORT=examples/reports/2nn_estimator_id-report.md

model:
	@test -f "$(PROMPT_FILE)" || (echo "PROMPT_FILE not found: $(PROMPT_FILE)"; exit 2)
	$(PYTHON) scripts/invoke_model.py --provider "$(PROVIDER)" --prompt-file "$(PROMPT_FILE)"

qa: pretty-check lint compile validate-skill test-all

qa-fix: pretty qa

qa-full: qa test-cov report-example

clean:
	find scripts examples tests -type d -name __pycache__ -prune -exec rm -rf {} +
	find scripts examples tests -type f -name '*.py[co]' -delete
	$(RM) .coverage
