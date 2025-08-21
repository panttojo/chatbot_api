# 🤖 Chatbot API

This API powers an intelligent chatbot designed to engage in meaningful debates.
Unlike a standard assistant, it doesn’t just answer questions — it argues a point of view and tries to convince you.
The system supports dynamic, context-aware conversations, making it feel like you’re talking to a skilled debater.

## 🚀 Features

- **Context-Aware Debates**: Remembers past messages to keep the discussion coherent and evolving.
- **Persistent Data:** Stores conversation history in a database for later review.
- **Scalable Architecture:** Built with a modular (hexagonal) design that makes it easy to swap components, e.g. change the database from **Postgres to Redis or MongoDB**.
- **Dockerized:** Includes Dockerfile and docker-compose for simple setup and deployment.
- **Automatic API Docs**: FastAPI generates interactive documentation via Swagger UI and ReDoc.
- **High Test Coverage**: Ships with a comprehensive test suite (99% coverage).

## 🛠️ Prerequisites

- Python 3.12
- [uv](https://docs.astral.sh/uv/) (for local development)
- Docker

## 📦 Installation

Clone the repository:
```bash
git clone git@github.com
:panttojo/chatbot_api.git
cd chatbot_api
```

### Project Structure



```bash
.
├── deployment
│   ├── Dockerfile                  # Production image
│   ├── Dockerfile.testing          # Testing image
│   └── entrypoint.sh
├── docker-compose.yaml
├── docs
├── envs                            # Environment files
├── Makefile
├── pyproject.toml
├── README.md
├── src
│   ├── api                         # Versioned API endpoints
│   │   └── v1
│   ├── core
│   │   ├── bots                    # Debate strategies and LLM integrations
│   │   ├── settings                # Configurations per environment
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   ├── local.py
│   │   │   ├── production.py
│   │   │   └── testing.py
│   ├── db                          # Persistent storage logic
│   ├── main.py                     # FastAPI entrypoint
│   ├── models
│   ├── tests
│   └── utils
└── uv.lock
```

### Configuration

The app is configured via environment variables.

Copy the sample file:
```bash
cp envs/.env.sample envs/.env.development # For Docker
cp envs/.env.sample envs/.env.local # For local development
```

Edit your .env file and set values:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| ENVIRONMENT | App environment (e.g. local, development, production) |  Yes | - |
| DATABASE_DSN | PostgreSQL connection string | Yes | - |
| LLM_API_KEY | API key for the LLM service (OpenAI) | Yes | - |
| SENTRY_DSN | Sentry DSN for error tracking | No | - |


## Running the Application

### With Docker (recommended):
```bash
make app
```

### Locally:
```bash
make install
source .venv/bin/activate
make start
```

## 📜 Makefile Commands

| Command | Description |
|---------|-------------|
| help | Show all available Makefile commands |
| install | Install project dependencies via uv |
| test | Run the test suite |
| run | Run in production mode |
| app | Start app with Docker Compose |
| down | Stop and remove Docker containers |
| clean | Remove containers, volumes, and images |
| clean_cache | Clear temp files (e.g. pycache) |
| lint | Run code linters |
| start | Start the local development server |
| update_libs | Update all dependencies |
| virtualenv | Create a Python virtual environment |

## 💻 API Usage

Send a `POST` request to `/v1/chat` to interact with the chatbot.
- Endpoint: `POST /v1/chat`
- Request Body:
    - Set `conversation_id` to `null` to start a new conversation.
    - Use an existing `conversation_id` to continue a chat.

Example request:
```json
{
    "conversation_id": "5556984b-9def-4b3c-ac07-e162b27977b5",
    "message": "The moon is made of cheese."
}
```

Example response:
```json
{
    "conversation_id": "5556984b-9def-4b3c-ac07-e162b27977b5",
    "messages": [
        {
            "role": "user",
            "message": "The moon is made of cheese."
        },
        {
            "role": "bot",
            "message": "Actually, the moon is not made of cheese. The Apollo missions brought back basaltic rocks and regolith..."
        }
    ]
}
```
