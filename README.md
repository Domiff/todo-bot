# ToDo Bot

Telegram bot for task management. Works together with the REST API ([todo-api](https://github.com/Domiff/todo-api)).

## Stack

- **Python 3.13** + [uv](https://github.com/astral-sh/uv)
- [aiogram 3](https://docs.aiogram.dev/) — Telegram Bot API
- [aiogram-dialog](https://aiogram-dialog.readthedocs.io/) — dialog-based UI (FSM)
- **Redis** — FSM state storage
- **RabbitMQ** + [aio-pika](https://aio-pika.readthedocs.io/) — events from todo-api ([CloudEvents](https://cloudevents.io/) JSON, parsed with pydantic)

Redis, RabbitMQ and logging (Grafana / Loki / Promtail) are not part of this repository: they run in
the separate **todo-infrastructure** stack.

## Features

- User registration via Telegram
- View task list
- Create a task (title, body, deadline, category)
- Edit a task (any field)
- Delete a task
- Notifications in Telegram when a task is created, updated or deleted (events from todo-api via RabbitMQ)

## Getting Started

### Environment variables

Copy `.env_template` to `.env` and fill in the values:

```bash
cp .env_template .env
```

```env
BOT_TOKEN=        # token from @BotFather
REDIS_HOST=todo-redis
REDIS_PORT=6379
REDIS_DB=0
BASE_URL=http://backend:8000
RABBITMQ_USER=    # same credentials as in todo-infrastructure's .env
RABBITMQ_PASSWORD=
RABBITMQ_HOST=todo-rabbitmq
RABBITMQ_PORT=5672
```

> `Settings` rejects unknown variables from the `.env` file, so do not add keys that are not
> declared in `bot/core/config.py`.

### Run with Docker Compose

The bot connects to Redis and RabbitMQ from todo-infrastructure and to todo-api over the external
network `todo-network`. Start order: **todo-infrastructure → todo-api → todo-bot**. This compose
file only contains the bot and has no `depends_on` on the infrastructure, so it must already be
running.

```bash
just up        # build and start the bot
just down      # stop the bot
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
│   ├── handlers.py     # dialog handlers + make_task_events_handler (event dispatch)
│   ├── consumers.py    # consume(handler, queue): reads a queue, acks/rejects messages
│   ├── events.py       # task event types and payloads (contract with todo-api)
│   ├── dialog.py
│   ├── router.py
│   ├── states.py
│   └── windows.py
├── core/
│   ├── config.py       # settings (pydantic-settings)
│   ├── http.py         # HttpClient, AuthURL / TodoURL enums, http_client()
│   ├── messaging/
│   │   ├── connection.py   # one robust connection + channel per process
│   │   ├── events.py       # Event[DataT]: CloudEvents envelope, get_event_type()
│   │   └── topology.py     # name of the queue the bot consumes
│   └── setup.py        # create_bot(), create_dispatcher()
└── main.py             # entry point: polling + RabbitMQ consumer task
```

## Events (RabbitMQ)

The broker (`todo-rabbitmq`) and its topology belong to todo-infrastructure
(`definitions.json`). The bot declares nothing; it only consumes the existing queue:

```
todo-api ──> todo.tasks (topic) ──tasks.#──> todo-bot.tasks ──> bot
```

Supported events:

| Event type             | Action                                                                              |
|------------------------|-------------------------------------------------------------------------------------|
| `todo.task.created.v1` | sends "Task ... was created" with the deadline to `tg_id`                           |
| `todo.task.updated.v1` | sends "Task ... was updated" with description, category, deadline and status (done / in progress) to `tg_id` |
| `todo.task.deleted.v1` | sends "Task ... was deleted" to `tg_id`                                             |

Messages are dispatched by the CloudEvents `type` field (`TaskEventTypes` in `bot/todo/events.py`).
User-provided text is HTML-escaped because the bot uses `parse_mode=HTML`.

**Known limitation:** an error while handling a message (unknown type, a payload that does not
match the model) currently stops the consumer task. The bot keeps answering in Telegram, but no
further events are read, and the failing message stays at the head of the queue, so a restart
hits it again. Check the queue's consumer count in the RabbitMQ management UI if notifications stop.

The payload models are a copy of todo-api's contract, and all their fields are required: a message
that lacks a field (for example, one published before the field was added) fails to parse and
triggers the limitation above.

To support a new event:

1. Add its type to `TaskEventTypes` and its payload model to `bot/todo/events.py`
   (must match todo-api).
2. Add a handler and register it in the `handlers` dict in `make_task_events_handler`.
3. If its routing key is not covered by the `tasks.#` binding, add a binding to
   `definitions.json` in todo-infrastructure.

## Monitoring

Grafana, Loki, Promtail and the RabbitMQ management UI run in todo-infrastructure; see its README
for URLs and ports.

## Linting

```bash
just lint      # ruff check
just fmt       # ruff format
just fix       # ruff check --fix
```
