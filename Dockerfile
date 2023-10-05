# syntax = docker/dockerfile:1.3

ARG PYTHON_VERSION

### Base image
FROM python:$PYTHON_VERSION-slim-bookworm AS base

ENV APP_HOME /app
ENV VIRTUAL_ENV /venv
ENV PYTHONPATH $APP_HOME
ENV PATH $VIRTUAL_ENV/bin:$PATH

ENV PIP_NO_CACHE_DIR 1

### Build python dependencies
FROM base AS builder

# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR $APP_HOME
COPY requirements.txt ./

# hadolint ignore=DL3013
RUN python -m venv /venv && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Production image
FROM base as runtime
LABEL org.opencontainers.image.source="https://github.com/hostmaster/robusta-google-chat"

ENV PATH /venv/bin:$PATH
COPY --from=builder /venv /venv
WORKDIR $APP_HOME
COPY . ./
CMD [ "python", "-u", "main.py" ]
