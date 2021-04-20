PROJECT := tesla-feeds
python_entry := python -m src.cli

default:project

project:
	@echo $(PROJECT)

# --- Pip requiremets
freeze-requirements:
	pip freeze > requirements-dev.txt
	pip-compile requirements.in
install-requirements-prod:
	pip install -r requirements.txt
install-requirements-dev:
	pip install -r requirements-dev.txt

# --- Linting
isort:
	isort .
black:
	black .
flake8:
	flake8 .
lint: isort black flake8


# --- Run scripts (in a virtual environment)
start:
	$(python_entry) start
