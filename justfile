set shell := ["bash", "-eu", "-o", "pipefail", "-c"]
set dotenv-load := false

# Do not update the env, when running
export UV_NO_SYNC := '1'

# List all available recipes
_default:
    @just --list --unsorted --list-submodules

# Install project dependencies
[group('dev')]
install *args='':
    uv sync --all-groups {{ args }}

# Format code with ruff
[group('format')]
format:
    uv run python -m ruff format

# Run all linters
[group('lint')]
lint:
    uv run python -m ruff check --exit-non-zero-on-fix
    uv run python -m ruff format --check --diff
    uv run python -m flake8 server
    uv run import-linter lint --no-logo

[group('lint')]
typos *args:
    uv run typos {{ args }}

# Run ruff linter
[group('lint')]
ruff:
    uv run python -m ruff check --exit-non-zero-on-fix
    uv run python -m ruff format --check --diff

# Run ruff linter
[group('lint')]
import-linter:
    uv run import-linter lint --no-logo

# Run wps linter
[group('lint')]
wps:
    uv run python -m flake8 server

# Run all checks
[group('dev')]
[group('tests')]
test: lint type-check unit

# Run unit tests
[group('tests')]
unit:

# Remove cache dirs
[group('dev')]
remove_cache:
    rm -rf .ruff_cache
    rm -rf .mypy_cache
    rm -rf .import_linter_cache

# Run all type checkers
[group('type-check')]
type-check:
    uv run python -m mypy . --show-traceback
    uv run python -m pyrefly check --remove-unused-ignores

# Run mypy
[group('type-check')]
mypy *args='':
    uv run python -m mypy . {{ args }}

# Run pyrefly
[group('type-check')]
pyrefly *args:
    uv run python -m pyrefly check --remove-unused-ignores {{ args }}

# Start dev server
[group('server')]
run *args='':
    uv run manage.py runserver {{ args }}

# Manage Django
[group('server')]
manage *args='':
    uv run manage.py {{ args }}

# Run interactive shell
[group('server')]
shell *args='':
    uv run manage.py shell {{ args }}

# Apply migrations
[group('db')]
migrate *args='':
    uv run manage.py migrate {{ args }}

# Create migrations
[group('db')]
make-migrations *args='':
    uv run manage.py makemigrations {{ args }}

# Start the Angular dev server
[group('client')]
client-dev:
    bun --cwd client run start

# Build the Angular client
[group('client')]
client-build:
    bun --cwd client run build

# Run Angular unit tests
[group('client')]
client-test:
    bun --cwd client run test

# Lint the Angular client
[group('client')]
client-lint:
    bun --cwd client run lint
