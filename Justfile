run:
    python -m bot.main

up:
    docker compose up

down:
    docker compose down

logs:
    docker compose logs -f bot

build:
    docker compose build bot

lint:
    uv run ruff check .

fmt:
    uv run ruff format .

fix:
    uv run ruff check --fix .
