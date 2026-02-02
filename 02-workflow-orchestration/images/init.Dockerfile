FROM python:3.13

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    gcc \
    python3-dev \
    build-essential && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY ../.env .
COPY ../pyproject.toml .

ENV PYTHONPATH=/app

RUN uv pip install --system --no-cache -r pyproject.toml

COPY ../init ./init

COPY ../common ./common

ENTRYPOINT ["python", "-m", "init.main"]