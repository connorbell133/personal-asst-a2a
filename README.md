# Personal Assistant A2A

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)
![GitHub issues](https://img.shields.io/github/issues/connorbell133/personal-asst-a2a)
![GitHub stars](https://img.shields.io/github/stars/connorbell133/personal-asst-a2a)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

> **Personal Assistant A2A** is a **privacy-first, multi-agent assistant** that connects to your Gmail, Google Calendar and Todoist accounts and answers natural-language questions such as "Do I have any overdue tasks for today?" or "What meetings do I have right after lunch tomorrow?".
>
> Under the hood each capability is implemented by an *agent* that uses MCP (Model Context Protocol) servers to interact with external services. A lightweight orchestration agent receives user prompts, discovers available agents at runtime and coordinates their tools to generate the final answer.

---

## ✨ Key Features

1. **Multi-Agent Architecture** – Each service (Gmail, Todoist, Calendar, Obsidian) has its own specialized Pydantic-AI agent
2. **MCP Integration** – Agents use Model Context Protocol servers for secure API interactions
3. **Dynamic Orchestration** – The orchestration agent coordinates multiple agents to handle complex queries
4. **Bring-Your-Own-LLM** – Works with any OpenAI-compatible model (OpenAI, Anthropic, Google Vertex, OpenRouter, etc.)
5. **Containerized Deployment** – All agents run in Docker containers with proper isolation
6. **Poetry Dependency Management** – Clean dependency management and virtual environment handling

---

## 📚 Table of Contents

1. [Quick Start](#quick-start)
2. [Project Layout](#project-layout)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Development](#development)
6. [Architecture](#architecture)
7. [Contributing](#contributing)
8. [License](#license)

---

## 🚀 Quick Start

### Prerequisites

* **Docker** and **Docker Compose** (for deployment)
* **Poetry** (for local development)
* Python **3.12+** (for local development)
* An **OpenAI-compatible** API key (e.g. `OPENAI_API_KEY`)
* **Google OAuth 2.0** credentials for Gmail and Google Calendar *(JSON file)*
* **Todoist** API token

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/personal-asst-a2a.git
cd personal-asst-a2a

# Install dependencies with Poetry (for local development)
poetry install

# Create environment file
cp .env.example .env  # Edit with your API keys
```

Place your `gcp-oauth.keys.json` file in the project root.

### Running with Docker Compose

```bash
# Build and start all agent services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# Stop all services
docker-compose down
```

If successful, you'll see agents running on:
- **Orchestration Agent**: http://127.0.0.1:10019
- **Gmail Agent**: http://127.0.0.1:10020  
- **Calendar Agent**: http://127.0.0.1:10023
- **Todoist Agent**: http://127.0.0.1:10022
- **Obsidian Agent**: http://127.0.0.1:10021

---

## 🗂️ Project Layout

```text
personal-asst-a2a/
├── app.py                      # Main launcher - starts all agent servers
├── client.py                   # Test client for interacting with agents
├── docker-compose.yml          # Container orchestration
├── dockerfile                  # Container build configuration
├── pyproject.toml              # Poetry dependencies and project config
├── poetry.lock                 # Locked dependency versions
├── src/
│   ├── agents/                 # Individual AI agents
│   │   ├── calendar_agent/     # Google Calendar integration
│   │   ├── gmail_agent/        # Gmail integration  
│   │   ├── obsidian_agent/     # Obsidian vault management
│   │   ├── orchestration_agent/# Coordinates other agents
│   │   ├── todoist_agent/      # Todoist task management
│   │   ├── common/             # Shared agent infrastructure
│   │   └── tools/              # Additional tool implementations
│   ├── core/                   # Core utilities (logging, LLMs)
│   └── mcp_servers/            # Model Context Protocol servers
│       ├── gmail.py            # Gmail MCP server
│       ├── gcal.py             # Google Calendar MCP server
│       └── todoist.py          # Todoist MCP server
├── gcp-oauth.keys.json         # Google OAuth credentials (not in git)
└── tasks/                      # Task definitions and workflows
```

---

## ⚙️ Configuration

Create a `.env` file with the following environment variables:

```dotenv
# LLM Provider (choose one)
OPENAI_API_KEY=sk-...
# or OPENROUTER_API_KEY=sk-or-...

# Google Services OAuth
GOOGLE_OAUTH_FILE=gcp-oauth.keys.json
GMAIL_CREDENTIALS_PATH=/gmail-server/credentials.json
GCALENDAR_CREDENTIALS_PATH=/gcal-server/credentials.json

# Todoist
TODOIST_API_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Server Configuration
SERVER_HOST=0.0.0.0

# Agent Ports (optional - defaults shown)
PORT_ORCHESTRATION=10019
PORT_GMAIL=10020
PORT_OBSIDIAN=10021
PORT_TODOIST=10022
PORT_CALENDAR=10023
```

### Google OAuth Setup

1. Create a Google Cloud Project
2. Enable Gmail and Calendar APIs
3. Create OAuth 2.0 credentials 
4. Download credentials as `gcp-oauth.keys.json`
5. Place in project root

---

## 🏃‍♂️ Running the Application

### Production Deployment (Docker Compose)

```bash
# Build and start all services
docker-compose up --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Local Development

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Run all agents locally
python app.py

# Or run individual agents
poetry run uvicorn src.agents.gmail_agent.agent:app --port 10020 --reload
```

### Testing Agents

```bash
# Use the test client
python client.py

# Or query agents directly via HTTP
curl -X POST http://localhost:10019/tasks \
  -H "Content-Type: application/json" \
  -d '{"query": "Do I have any meetings today?"}'
```

---

## 🧑‍💻 Development

### Poetry Commands

```bash
# Install all dependencies (including dev)
poetry install

# Add new dependency
poetry add package-name

# Add dev dependency  
poetry add --group dev package-name

# Update dependencies
poetry update

# Run commands in virtual environment
poetry run python script.py
poetry run pytest
```

### Code Quality

```bash
# Format code
poetry run ruff format .

# Lint code
poetry run ruff check .

# Type checking (if configured)
poetry run pylint src/

# Run tests
poetry run pytest
```

### Adding New Agents

1. Create agent directory: `src/agents/new_agent/`
2. Implement agent with config: `agent.py`, `config.yml`
3. Create MCP server if needed: `src/mcp_servers/new_service.py`
4. Register agent in `app.py`
5. Update Docker Compose ports if needed

---

## 🏗️ Architecture

### Agent Layer
- **Pydantic-AI Agents**: Each service has a specialized agent
- **Agent Cards**: Define agent metadata, ports, and capabilities  
- **Agent Manager**: Handles registration and server creation

### MCP Layer  
- **MCP Servers**: Implement Model Context Protocol for external APIs
- **Tool Integration**: Agents use MCP servers as tools
- **Secure Communication**: Isolated API interactions

### Orchestration Layer
- **Background Threads**: Each agent runs in its own thread
- **Port-based Communication**: Agents communicate via HTTP
- **Dynamic Discovery**: Agents discover each other at runtime

### Infrastructure Layer
- **Docker Containers**: Isolated execution environments
- **Volume Mounts**: Persistent credential storage
- **Poetry**: Dependency management and virtual environments

---

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Install** dependencies: `poetry install`
4. **Make** your changes
5. **Test** your changes: `poetry run pytest`
6. **Format** code: `poetry run ruff format .`
7. **Commit** changes: `git commit -m 'Add amazing feature'`
8. **Push** to branch: `git push origin feature/amazing-feature`
9. **Open** a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
