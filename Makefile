TESTS = tests

VENV ?= .venv
CODE = tests app

.PHONY: venv
venv:
	python3 -m virtualenv $(VENV)
	$(VENV)/bin/python3 -m pip install --upgrade pip
	$(VENV)/bin/python3 -m pip install poetry
	$(VENV)/bin/poetry install

.PHONY: up
up:
	FLASK_APP=app.app $(VENV)/bin/flask run
