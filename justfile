set shell := ["bash", "-eu", "-o", "pipefail", "-c"]
set dotenv-load := false

# Do not update the env, when running
export UV_NO_SYNC := '1'

# List all available recipes
_default:
    @just --list --unsorted --list-submodules

[group('dev')]
install *args='':
    uv sync --all-groups {{ args }}

# Format code with ruff
[group('dev')]
format:
    uv run python -m ruff format
    uv run python -m ruff check

# Run all linters
[group('dev')]
lint:
    uv run python -m ruff check --exit-non-zero-on-fix
    uv run python -m ruff format --check --diff

# Run all type checkers
[group('type-check')]
type-check:
    uv run python -m mypy .
    uv run python -m pyrefly check --remove-unused-ignores

# Run mypy
[group('type-check')]
mypy *args='':
    uv run python -m mypy . {{args}}

# Run pyrefly
[group('type-check')]
pyrefly *args:
    uv run python -m pyrefly check --remove-unused-ignores {{args}}

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
