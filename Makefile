PROJECT := no-space-alert
python_entry := python -m src.cli

default:project

project:
	@echo $(PROJECT)

# --- Pip requiremets
pip-freeze:
	pip-compile requirements.in
	pip-compile requirements.in requirements-dev.in --output-file requirements-dev.txt

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
show-logs: 
	cat logs/logs.log | tail -n 20

# --- Run scripts in a docker container
dc-down:
	docker-compose down --remove-orphans
dc-build:
	docker-compose build
dc-up:
	docker-compose up -d
dc-compose: dc-down dc-build dc-up
dc-logs:
	docker-compose logs --tail 20
