FROM python:3.10-slim-buster

ENV DEBIAN_FRONTEND noninteractive
ENV POETRY_VERSION=1.7.1

RUN apt-get update && \
    apt-get install -y \
        curl \
        inotify-tools \
        make \
    && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PATH=$PATH:/root/.local/bin/

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install

COPY . .

RUN poetry install

ENTRYPOINT ["make"]
