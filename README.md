# Django AI Assistant

A Django-based AI assistant that integrates a local LLM powered by Ollama with an agent-based architecture and custom tools.

## Features

- Django backend
- Django REST Framework
- Local LLM inference with Ollama
- Qwen2.5-Coder 3B
- AI Agent architecture
- Custom AI tools
- ChromaDB for vector storage
- SQLite database
- Chat interface
- Dashboard
- Docker support
- Git/GitHub integration

## Architecture

```text
                    ┌─────────────────┐
                    │     Browser     │
                    └────────┬────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │       Django        │
                  │                     │
                  │   Views / DRF       │
                  │   AI Agent          │
                  │   Tools             │
                  └─────────┬───────────┘
                            │
                 ┌──────────┴──────────┐
                 │                     │
                 ▼                     ▼
          ┌─────────────┐       ┌─────────────┐
          │  ChromaDB   │       │   SQLite    │
          │ Vector DB   │       │  Database   │
          └─────────────┘       └─────────────┘

                            │
                            ▼
                  ┌──────────────────┐
                  │      Ollama      │
                  │                  │
                  │ qwen2.5-coder:3b │
                  └──────────────────┘
```
## Project Structure


django-ai-assistant/
│
├── ai_assistant/
│   ├── agent.py
│   ├── llm.py
│   ├── tools.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── djangoProject2/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
├── static/
│
├── chroma_db/
├── db.sqlite3
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
└── README.md

Requirements
Python 3.12+
Django
Django REST Framework
Docker
Ollama
Qwen2.5-Coder 3B
Ollama Setup

Install Ollama and download the model:
ollama pull qwen2.5-coder:3b
Make sure Ollama is running:
ollama serve

## Running with Docker

Build the Docker image:
  docker compose build

  docker compose up

The application will be available at:http://localhost:8000

## AI Pipeline

The basic request flow is:

User
  │
  ▼
Django
  │
  ▼
AI Agent
  │
  ├── Tools
  │
  ├── ChromaDB
  │
  ▼
Ollama
  │
  ▼
Qwen2.5-Coder 3B
  │
  ▼
AI Response

## Technologies
Python
Django
Django REST Framework
Ollama
Qwen2.5-Coder
ChromaDB
SQLite
Docker
Git
## License

This project is for educational and portfolio purposes.
