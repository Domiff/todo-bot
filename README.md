# ToDo Bot

Telegram bot for task management. Works together with the REST API ([todo-api](https://github.com/Domiff/todo-api)).

## Stack

- **Python 3.13** + [uv](https://github.com/astral-sh/uv)
- [aiogram 3](https://docs.aiogram.dev/) — Telegram Bot API
- [aiogram-dialog](https://aiogram-dialog.readthedocs.io/) — dialog-based UI (FSM)
- **Redis** — FSM state storage
- **Grafana / Loki / Promtail** — log collection and visualization

## Features

- User registration via Telegram
- View task list
- Create a task (title, body, deadline, category)
- Edit a task (any field)
- Delete a task

## Getting Started

### Environment variables

Copy `.env_template` to `.env` and fill in the values:

```bash
cp .env_template .env
```

```env
BOT_TOKEN=        # token from @BotFather
REDIS_HOST=todo-bot-redis
REDIS_PORT=6379
REDIS_DB=0
BASE_URL=http://<todo-api address>/
```

### Run with Docker Compose

Make sure the shared network exists:

```bash
docker network create todo-network
```

```bash
just up        # build and start all services
just down      # stop all services
just logs      # follow bot logs
just build     # rebuild the bot image only
```

### Run locally (development)

```bash
uv sync
just run
```

> The bot reads `.env` from the **parent** directory of the project root (configured in `pydantic-settings`).

## Project structure

```
bot/
├── auth/
│   ├── service.py      # AuthService: register, refresh_token, check_token
│   ├── handlers.py
│   ├── dialog.py
│   ├── router.py
│   ├── states.py
│   └── windows.py
├── todo/
│   ├── service.py      # TodoService: CRUD operations, prepare_message
│   ├── handlers.py
│   ├── dialog.py
│   ├── router.py
│   ├── states.py
│   └── windows.py
├── core/
│   ├── config.py       # settings (pydantic-settings)
│   ├── http.py         # HttpClient, AuthURL / TodoURL enums, http_client()
│   └── setup.py        # create_bot(), create_dispatcher()
└── main.py             # entry point
```

## Monitoring

| Service  | URL                   |
|----------|-----------------------|
| Grafana  | http://localhost:3001 |
| Loki     | http://localhost:3101 |
| Promtail | http://localhost:9081 |

Container logs are collected by Promtail → Loki → Grafana.

## Linting

```bash
just lint      # ruff check
just fmt       # ruff format
just fix       # ruff check --fix
```
