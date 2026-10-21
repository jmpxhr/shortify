# syntax = docker/dockerfile:1
# Multi-stage build that produces development and production images:
# https://docs.docker.com/develop/develop-images/multistage-build/

FROM python:3.14.8-slim-bookworm AS development_build

# `DJANGO_ENV` arg is used to make prod / dev builds:
ARG DJANGO_ENV \
  # Needed for fixing permissions of files created by Docker:
  UID=1000 \
  GID=1000

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_DEFAULT_TIMEOUT=100 \
  PIP_ROOT_USER_ACTION=ignore \
  # uv:
  UV_COMPILE_BYTECODE=1 \
  UV_LINK_MODE=copy \
  UV_PYTHON_DOWNLOADS=0 \
  UV_PROJECT_ENVIRONMENT=/opt/venv \
  UV_NO_SYNC=1 \
  PATH="/opt/venv/bin:${PATH}"

SHELL ["/bin/bash", "-eo", "pipefail", "-c"]

RUN apt-get update \
  && apt-get install --no-install-recommends -y \
  bash \
  brotli \
  build-essential \
  curl \
  gettext \
  git \
  libpq-dev \
  # Cleaning cache:
  && apt-get clean -y \
  && rm -rf /var/lib/apt/lists/*

# https://docs.astral.sh/uv/guides/integration/docker/
COPY --from=ghcr.io/astral-sh/uv:0.13.4 /uv /uvx /bin/

WORKDIR /code

RUN groupadd -g "${GID}" -r web \
  && useradd -d '/code' -g web -l -r -u "${UID}" web \
  && chown web:web -R '/code' \
  # Static and media files:
  && mkdir -p '/var/www/django/static' '/var/www/django/media' \
  && chown web:web '/var/www/django/static' '/var/www/django/media'

# Copy only dependency manifests to cache them in a Docker layer.
COPY --chown=web:web ./pyproject.toml ./uv.lock  /code/

# `uv` installs into /opt/venv instead of /code/.venv, so bind-mounting the
# project over /code does not hide the installed dependencies.
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --locked $(if [ "$DJANGO_ENV" = 'production' ]; then echo '--no-dev'; fi) --no-install-project \
  && chown -R web:web /opt/venv

# This is a special case: the script is used as the entrypoint.
COPY ./docker/django/entrypoint.sh /docker-entrypoint.sh

# Setting up proper permissions:
RUN chmod +x '/docker-entrypoint.sh' \
  # Replacing line separator CRLF with LF for Windows users:
  && sed -i 's/\r$//g' '/docker-entrypoint.sh'

# Running as non-root user:
USER web

# Custom entrypoint, the default command can be overridden by Compose.
ENTRYPOINT ["/docker-entrypoint.sh"]


# The following stage is only for production:
FROM development_build AS production_build
COPY --chown=web:web . /code
