# Directories
BACKEND_DIR := backend
APPS_DIR := $(BACKEND_DIR)/apps
FRONTEND_DIR := frontend
STUBS_DIR := stubs
TEST_DIR := tests

# Commands
POETRY := poetry
BLACK := $(POETRY) run black
ISORT := $(POETRY) run isort
FLAKE8 := $(POETRY) run flake8
MYPY := $(POETRY) run mypy
NPM := npm

# Options
BLACK_OPTIONS := --line-length 79 --exclude "migrations"
ISORT_OPTIONS := --trailing-comma --multi-line=3 --skip "migrations"
FLAKE8_OPTIONS := --exclude "migrations"
MYPY_OPTIONS := --config-file mypy.ini

# Phony targets
.PHONY: format lint type-check install install-frontend install-backend check-backend check-frontend check migrate run clear-dev-db

# Install dependencies
install: install-frontend install-backend

install-frontend:
	cd $(FRONTEND_DIR) && $(NPM) install

install-backend:
	$(POETRY) install

# Formatting
format: format-frontend format-backend

format-frontend:
	$(NPM) run format

format-backend:
	PYTHONPATH=$(BACKEND_DIR) $(BLACK) $(BLACK_OPTIONS) $(BACKEND_DIR) $(STUBS_DIR) $(TEST_DIR)
	PYTHONPATH=$(BACKEND_DIR) $(ISORT) $(ISORT_OPTIONS) $(BACKEND_DIR) $(STUBS_DIR) $(TEST_DIR)

# Linting
lint: lint-frontend lint-backend

lint-frontend:
	$(NPM) run lint  -- --fix

lint-backend:
	PYTHONPATH=$(BACKEND_DIR) $(FLAKE8) $(FLAKE8_OPTIONS) $(BACKEND_DIR) $(STUBS_DIR) $(TEST_DIR)

# Type-checking
type-check:
	PYTHONPATH=$(BACKEND_DIR) $(MYPY) $(MYPY_OPTIONS) $(BACKEND_DIR) $(STUBS_DIR) $(TEST_DIR)

# Combined checks
check-frontend: format-frontend lint-frontend

check-backend: format-backend lint-backend type-check

check: check-frontend check-backend

# Migrations
migrate:
	@for app in $$(ls $(APPS_DIR)); do \
		if [ "$$app" != "__pycache__" ] && [ -d "$(APPS_DIR)/$$app" ]; then \
			PYTHONPATH=$(BACKEND_DIR) $(POETRY) run python $(BACKEND_DIR)/manage.py makemigrations $$app; \
		fi \
	done
	PYTHONPATH=$(BACKEND_DIR) $(POETRY) run python $(BACKEND_DIR)/manage.py migrate

# Migrate and run the server
run: migrate
	PYTHONPATH=$(BACKEND_DIR) $(POETRY) run python $(BACKEND_DIR)/manage.py runserver

# Clear development database
clear-dev-db:
	PYTHONPATH=$(BACKEND_DIR) $(POETRY) run python $(BACKEND_DIR)/manage.py flush --noinput