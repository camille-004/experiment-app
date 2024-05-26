BACKEND_DIR := backend
FRONTEND_DIR := frontend
STUBS_DIR := stubs
TEST_DIR := tests

POETRY := poetry
BLACK := $(POETRY) run black
ISORT := $(POETRY) run isort
FLAKE8 := $(POETRY) run flake8
MYPY := $(POETRY) run mypy
NPM := npm

# Options
BLACK_OPTIONS := --line-length 79
ISORT_OPTIONS := --trailing-comma --multi-line=3
FLAKE8_OPTIONS :=
MYPY_OPTIONS := --config-file mypy.ini

.PHONY: format lint type-check install install-frontend install-backend

install: install-frontend install-backend

install-frontend:
	cd $(FRONTEND_DIR) && $(NPM) install

install-backend:
	$(POETRY) install

format-backend:
	PYTHONPATH=$(BACKEND_DIR) $(BLACK) $(BLACK_OPTIONS) $(BACKEND_DIR) $(STUBS_DIR) $(TEST_DIR)
	PYTHONPATH=$(BACKEND_DIR) $(ISORT) $(ISORT_OPTIONS) $(BACKEND_DIR) $(STUBS_DIR) $(TEST_DIR)

format-frontend:
	$(NPM) run format

lint: lint-python lint-frontend

lint-backend:
	PYTHONPATH=$(BACKEND_DIR) $(FLAKE8) $(FLAKE8_OPTIONS) $(BACKEND_DIR) $(STUBS_DIR) $(TEST_DIR)

lint-frontend:
	$(NPM) run lint  -- --fix

type-check:
	PYTHONPATH=$(BACKEND_DIR) $(MYPY) $(MYPY_OPTIONS) $(BACKEND_DIR) $(STUBS_DIR) $(TEST_DIR)

check: format lint type-check

migrate:
	PYTHONPATH=$(BACKEND_DIR) $(POETRY) run python $(BACKEND_DIR)/manage.py makemigrations
	PYTHONPATH=$(BACKEND_DIR) $(POETRY) run python $(BACKEND_DIR)/manage.py migrate

run: migrate
	PYTHONPATH=$(BACKEND_DIR) $(POETRY) run python $(BACKEND_DIR)/manage.py runserver

clear-dev-db:
	PYTHONPATH=$(BACKEND_DIR) $(POETRY) run python $(BACKEND_DIR)/manage.py flush --noinput