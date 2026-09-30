# Django AI Assistant
## API Demo

### 1. Sending a Request

The AI assistant accepts user messages through a Django REST Framework API.

![DRF Request](Screenshot%202026-09-30%20221900.png)
### 2. API Response

The API processes the request through the AI agent and returns the generated response.

![DRF Response](Screenshot%202026-09-30%20221918.png)
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


## 📁 Project Structure

```text
django-ai-assistant/
│
├── ai_assistant/                 # Main AI assistant application
│   ├── agent.py                  # AI agent logic and decision flow
│   ├── llm.py                    # Ollama / LLM communication
│   ├── tools.py                  # Custom AI tools
│   ├── models.py                 # Database models
│   ├── serializers.py            # DRF serializers
│   ├── views.py                  # API and application views
│   └── urls.py                   # Application routes
│
├── djangoProject2/               # Django project configuration
│   ├── settings.py               # Project settings
│   ├── urls.py                   # Main URL configuration
│   ├── asgi.py                   # ASGI configuration
│   └── wsgi.py                   # WSGI configuration
│
├── templates/                    # HTML templates
├── static/                       # CSS and JavaScript files
│
├── chroma_db/                    # ChromaDB vector database
├── db.sqlite3                    # SQLite database
│
├── Dockerfile                    # Docker image configuration
├── docker-compose.yml            # Docker Compose configuration
├── requirements.txt              # Python dependencies
├── manage.py                     # Django management utility
└── README.md                     # Project documentation
```

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
```text

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
```

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
