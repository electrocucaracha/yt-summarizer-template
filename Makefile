PROJECT := {{cookiecutter.repo_name}}
PYTHON_FILES := scripts "$(PROJECT)/scripts"
TOOLS := uv run --no-project --python 3.12 --with-requirements "$(PROJECT)/requirements-dev.txt"
CONFIG := $(PROJECT)/pyproject.toml

.PHONY: check lint fmt
check: lint
	$(TOOLS) python scripts/check_template.py

lint:
	$(TOOLS) black --check --config "$(CONFIG)" $(PYTHON_FILES)
	$(TOOLS) isort --check-only --settings-path "$(CONFIG)" $(PYTHON_FILES)
	$(TOOLS) ruff check --config "$(CONFIG)" $(PYTHON_FILES)
	$(TOOLS) pylint --rcfile "$(CONFIG)" $(PYTHON_FILES)
	$(TOOLS) mypy --config-file "$(CONFIG)" $(PYTHON_FILES)
	$(TOOLS) bandit --recursive --severity-level medium --confidence-level medium $(PYTHON_FILES)

fmt:
	$(TOOLS) isort --settings-path "$(CONFIG)" $(PYTHON_FILES)
	$(TOOLS) black --config "$(CONFIG)" $(PYTHON_FILES)