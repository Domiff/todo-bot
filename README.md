# ToDo Bot

Telegram bot for task management. Works together with the REST API ([todo-api](https://github.com/Domiff/todo-api)).

## Stack

- **Python 3.13** + [uv](https://github.com/astral-sh/uv)
- [aiogram 3](https://docs.aiogram.dev/) — Telegram Bot API
- [aiogram-dialog](https://aiogram-dialog.readthedocs.io/) — dialog-based UI (FSM)
- **Redis** — FSM state storage
- **RabbitMQ** + [aio-pika](https://aio-pika.readthedocs.io/) — events from todo-api ([CloudEvents](https://cloudevents.io/) JSON, parsed with pydantic)
- **Grafana / Loki / Promtail** — log collection and visualization

## Features

- User registration via Telegram
- View task list
- Create a task (title, body, deadline, category)
- Edit a task (any field)
- Delete a task
- Notification in Telegram when a task is created (event from todo-api via RabbitMQ)

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
RABBITMQ_USER=    # also used as the broker's default user in docker-compose.yml
RABBITMQ_PASSWORD=
RABBITMQ_HOST=todo-bot-rabbitmq
RABBITMQ_PORT=5672
```

> `Settings` rejects unknown variables from the `.env` file, so do not add keys that are not
> declared in `bot/core/config.py`.

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
│   │   ├── connection.py   # one robust connection + channel; declares topology on connect
│   │   ├── events.py       # Event[DataT]: CloudEvents envelope, get_event_type()
│   │   └── topology.py     # exchanges, queues and bindings of the bot
│   └── setup.py        # create_bot(), create_dispatcher()
└── main.py             # entry point: polling + RabbitMQ consumer task
```

## Events (RabbitMQ)

The RabbitMQ broker runs in this stack (`todo-bot-rabbitmq`) and is shared with todo-api over
`todo-network`. Start the bot stack before todo-api, otherwise todo-api cannot publish events.

Topology declared by the bot on connect:

```
todo.tasks (direct) ──tasks.created──> todo-bot.tasks.created ──> bot
```

- `todo.tasks` exchange belongs to todo-api; the bot redeclares it with the same parameters
  (`direct`, durable) so the binding works whichever service starts first.
- `todo-bot.tasks.created` is the bot's durable queue.

Supported events:

| Event type             | Action                                                  |
|------------------------|---------------------------------------------------------|
| `todo.task.created.v1` | sends "Task ... was created" with the deadline to `tg_id` |

Messages are dispatched by the CloudEvents `type` field. A message with an unknown type or an
invalid payload is rejected without requeue (there is no dead letter queue yet, so it is dropped).

To support a new event:

1. Add its type and payload model to `bot/todo/events.py` (must match todo-api).
2. Add a handler and register it in the `handlers` dict in `make_task_events_handler`.
3. Bind the queue to the event's routing key in `bot/core/messaging/topology.py`.

## Monitoring

| Service  | URL                   |
|----------|-----------------------|
| Grafana  | http://localhost:3001 |
| Loki     | http://localhost:3101 |
| Promtail | http://localhost:9081 |
| RabbitMQ management | http://localhost:15671 |

Container logs are collected by Promtail → Loki → Grafana.

## Linting

```bash
just lint      # ruff check
just fmt       # ruff format
just fix       # ruff check --fix
```
