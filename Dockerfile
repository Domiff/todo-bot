FROM python:3.13-slim-trixie AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /bot

COPY pyproject.toml ./

ENV UV_PROJECT_ENVIRONMENT=/usr/local

ENV UV_SYSTEM_PYTHON=1

RUN uv sync --no-dev


FROM python:3.13-slim-trixie

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/usr/local/bin:$PATH

COPY --from=builder /usr/local /usr/local

COPY bot /app/bot

CMD ["python", "-m", "bot.main"]
