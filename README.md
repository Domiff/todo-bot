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

Create an `.env.bot` file in the project root:

```env
BOT_TOKEN=<your token from @BotFather>
REDIS_HOST=todo-bot-redis
REDIS_PORT=6379
REDIS_DB=0
BASE_URL=http://<todo-api address>/
```

### Run with Docker Compose

```bash
just up        # start all services
just down      # stop all services
just logs      # follow bot logs (-f / --follow)
just build     # rebuild the bot image
```

The bot, Redis, and the monitoring stack run inside the `todo-network` Docker network.
Make sure the network exists before starting:

```bash
docker network create todo-network
```

### Run locally (development)

```bash
uv sync
just run
```

## Project structure

```
bot/
├── api/            # HTTP client for todo-api
├── crud/           # create / read / update / delete operations
├── dialogs/
│   ├── registration/   # registration dialog
│   └── todo/
│       ├── create/     # task creation
│       ├── read/       # task list
│       ├── update/     # task editing
│       └── delete/     # task deletion
├── config.py       # settings (pydantic-settings)
└── main.py         # entry point
```

## Monitoring

| Service  | URL                    |
|----------|------------------------|
| Grafana  | http://localhost:3001  |
| Loki     | http://localhost:3101  |
| Promtail | http://localhost:9081  |

Container logs are collected by Promtail → Loki → Grafana.

## Linting

```bash
just lint      # ruff check
just fmt       # ruff format
just fix       # ruff check --fix
```
