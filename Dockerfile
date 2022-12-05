FROM python:3.10-alpine AS base

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /app

# disable virtualenv for poetry
COPY ./pyproject.toml pyproject.toml
RUN poetry config virtualenvs.create false

# install dependencies
RUN poetry install --only main

# add source code
COPY ./roomgraph roomgraph

ENTRYPOINT [ "make" ]