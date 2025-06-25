# AI Assistant A2A

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

> **AI Assistant A2A** is a **privacy-first, multi-agent assistant** powered by the [A2A SDK](https://github.com/pydantic/agent2agent) that connects to your Gmail, Google Calendar, and Todoist accounts to answer natural-language questions like "Do I have any overdue tasks for today?" or "What meetings do I have right after lunch tomorrow?".
>
> Built with **Pydantic AI** and **MCP (Model Context Protocol)**, each capability is implemented as a standalone microservice that can run locally, remotely, or in containers. A lightweight orchestration agent coordinates workflows across services to provide intelligent, context-aware responses.

---

## ✨ Key Features

- **🔒 Privacy-First**: 100% local execution - no data leaves your machine except intentional LLM API calls
- **🏗️ Microservice Architecture**: Each agent runs as an independent Starlette server with A2A integration
- **🤖 Dynamic Orchestration**: Central orchestration agent discovers available services and chains tools automatically
- **🧠 Multi-Model Support**: Works with any OpenAI-compatible model (OpenAI, Anthropic, Google Vertex, OpenRouter)
- **🔌 MCP Integration**: Leverages Model Context Protocol for secure, standardized tool access
- **📈 Observable**: Built-in Logfire integration for comprehensive monitoring and debugging
- **🚀 Extensible**: Add new agents in ~100 lines of code with automatic discovery

---

## 📚 Table of Contents

1. [Quick Start](#-quick-start)
2. [Architecture](#-architecture)
3. [Project Structure](#-project-structure)
4. [Configuration](#-configuration)
5. [Running the System](#-running-the-system)
6. [Adding New Agents](#-adding-new-agents)
7. [Development](#-development)
8. [API Documentation](#-api-documentation)
9. [Contributing](#-contributing)
10. [License](#-license)

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+** (required by `pyproject.toml`)
- **OpenAI-compatible API key** (OpenAI, OpenRouter, etc.)
- **Google OAuth 2.0 credentials** for Gmail/Calendar access
- **Todoist API token** for task management

### Installation

```bash
# Clone and enter the project
git clone https://github.com/your-org/ai-asst-a2a.git
cd ai-asst-a2a

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies with Poetry
poetry install

# Or with pip
pip install -e .
```

### Configuration

Create a `.env` file in the project root:

```env
# LLM Provider (choose one)
OPENAI_API_KEY=sk-...
# or OPENROUTER_API_KEY=...

# Google Services
GOOGLE_OAUTH_CREDENTIALS=/path/to/your/gcp-oauth.keys.json

# Todoist
TODOIST_API_TOKEN=your_todoist_token_here

# Optional - Custom Ports
PORT_GMAIL=10020
PORT_TODOIST=10022
PORT_CALENDAR=10023
PORT_ORCHESTRATION=10024
```

Place your Google OAuth credentials JSON file in the project root as `gcp-oauth.keys.json`.

### Launch

```bash
python app.py
```

You'll see output like:

```
✅ Agent servers are running!
   - Gmail Agent: http://127.0.0.1:10020
   - Todoist Agent: http://127.0.0.1:10022
   - Calendar Agent: http://127.0.0.1:10023
   - Orchestration Agent: http://127.0.0.1:10024
```

The system will automatically demonstrate functionality with an example query.

---

## 🏗 Architecture

The system follows a **microservice architecture** with the following components:

### Core Components

- **Orchestration Agent**: Central coordinator that discovers services and chains tools
- **Domain Agents**: Specialized agents for Gmail, Calendar, Todoist, and GitHub
- **MCP Servers**: Secure backend services providing tool access via Model Context Protocol
- **A2A Framework**: Service discovery and inter-agent communication layer

### Agent Communication Flow

```
User Query → Orchestration Agent → Service Discovery → Tool Chaining → Response
```

1. User submits natural language query
2. Orchestration agent analyzes intent
3. Discovers available domain agents via A2A
4. Chains appropriate tools across services
5. Returns unified, intelligent response

---

## 📁 Project Structure

```
ai-asst-a2a/
├── app.py                          # Main application launcher
├── pyproject.toml                  # Project metadata and dependencies
├── gcp-oauth.keys.json            # Google OAuth credentials (gitignored)
├── logs/                          # Agent execution logs
│   ├── calendar_agent_10023.log
│   ├── gmail_agent_10020.log
│   ├── orchestration_agent_10024.log
│   └── todoist_agent_10022.log
├── src/
│   ├── agents/                    # Agent implementations
│   │   ├── common/               # Shared agent utilities
│   │   │   ├── agent.py         # Base agent configuration loader
│   │   │   ├── agent_executor.py # Agent execution framework
│   │   │   ├── server.py        # A2A server creation utilities
│   │   │   └── tool_client.py   # A2A client for inter-agent communication
│   │   ├── calendar_agent/      # Google Calendar integration
│   │   │   ├── agent.py
│   │   │   └── config.yml
│   │   ├── gmail_agent/         # Gmail integration
│   │   │   ├── agent.py
│   │   │   └── config.yml
│   │   ├── obsidian_agent/      # Obsidian note management
│   │   │   ├── agent.py
│   │   │   └── config.yml
│   │   ├── orchestration_agent/ # Central coordination
│   │   │   ├── agent.py
│   │   │   └── config.yml
│   │   ├── todoist_agent/       # Task management
│   │   │   ├── agent.py
│   │   │   └── config.yml
│   │   └── tools/               # Shared tools
│   │       └── github_tools.py  # GitHub repository operations
│   ├── core/                    # Core utilities
│   │   ├── llms.py             # LLM client configuration
│   │   └── logger.py           # Logging configuration
│   └── mcp_servers/            # Model Context Protocol servers
│       ├── gcal.py            # Google Calendar MCP server
│       ├── gmail.py           # Gmail MCP server
│       └── todoist.py         # Todoist MCP server
└── show_tree.py               # Development utility for project visualization
```

### Key Components Explained

- **`agents/common/`**: Shared infrastructure for agent creation, configuration, and server management
- **`mcp_servers/`**: Secure backend services that provide tool access via the Model Context Protocol
- **`core/`**: Fundamental utilities for LLM interaction and logging
- **`config.yml` files**: YAML configuration for each agent defining models, prompts, and endpoints

---

## ⚙️ Configuration

### Environment Variables

All configuration is handled through environment variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key | Yes (or alternative) |
| `OPENROUTER_API_KEY` | OpenRouter API key | Alternative to OpenAI |
| `GOOGLE_OAUTH_CREDENTIALS` | Path to Google OAuth JSON | Yes |
| `TODOIST_API_TOKEN` | Todoist API token | Yes |
| `GITHUB_TOKEN` | GitHub API token (for GitHub tools) | Optional |
| `PORT_*` | Custom ports for each agent | Optional |

### Agent Configuration

Each agent has a `config.yml` file defining:

```yaml
name: Agent Name
description: Agent description
model: google-gla:gemini-2.5-pro  # or openai:gpt-4, etc.
endpoint: http://localhost:PORT
system_prompt: |
  Your detailed system prompt here...
```

### Google OAuth Setup

1. Create a Google Cloud Project
2. Enable Gmail and Calendar APIs
3. Create OAuth 2.0 credentials
4. Download the JSON file as `gcp-oauth.keys.json`

---

## 🏃‍♂️ Running the System

### All Services

Start all agents with a single command:

```bash
python app.py
```

This launches all agents in background threads and demonstrates inter-agent communication.

### Individual Agents

Run specific agents independently:

```bash
# Gmail agent only
uvicorn src.agents.gmail_agent.agent:app --port 10020 --reload

# Calendar agent only
uvicorn src.agents.calendar_agent.agent:app --port 10023 --reload

# Orchestration agent only
uvicorn src.agents.orchestration_agent.agent:app --port 10024 --reload
```

### API Exploration

Each agent provides:
- **OpenAPI documentation**: `http://localhost:PORT/docs`
- **A2A schema**: `http://localhost:PORT/.well-known/ai-plugin.json`
- **Health check**: `http://localhost:PORT/health`

---

## ➕ Adding New Agents

Creating a new agent is straightforward:

### 1. Create Agent Structure

```bash
mkdir -p src/agents/your_agent
touch src/agents/your_agent/__init__.py
touch src/agents/your_agent/agent.py
touch src/agents/your_agent/config.yml
```

### 2. Define Configuration

```yaml
# src/agents/your_agent/config.yml
name: Your Agent
description: Description of your agent's capabilities
model: google-gla:gemini-2.5-flash
endpoint: http://localhost:10025
system_prompt: |
  You are a specialized agent for...
```

### 3. Implement Agent

```python
# src/agents/your_agent/agent.py
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic import BaseModel
from a2a.types import AgentSkill
from src.agents.common.agent import load_agent_config

load_dotenv(override=True)

config = load_agent_config("src/agents/your_agent/config.yml")

class YourAgentCard(BaseModel):
    name: str = config.name
    description: str = config.description
    skills: list[AgentSkill] = []
    organization: str = config.name
    url: str = config.endpoint

your_agent = Agent(
    model=config.model,
    name=config.name,
    system_prompt=config.system_prompt,
)

@your_agent.tool
def your_tool(param: str) -> str:
    """Tool description for the agent."""
    # Your tool logic here
    return f"Result for {param}"

# Export A2A app
app = your_agent.to_a2a()
```

### 4. Register with Orchestrator

Add your agent to `app.py`:

```python
{
    "name": "Your Agent",
    "agent": create_your_agent_server,
    "port": 10025,
}
```

The orchestration agent will automatically discover and integrate your new agent!

---

## 🧑‍💻 Development

### Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type checking
mypy src/

# Run tests
pytest
```

### Development Dependencies

Install development tools:

```bash
poetry install --group dev
```

Includes:
- `ruff`: Fast Python linter and formatter
- `pylint`: Additional linting
- `pytest`: Testing framework
- `black`: Code formatting (backup)

### Debugging

The system includes comprehensive logging via Logfire:

- **Console output**: Real-time agent activity
- **Log files**: Detailed execution logs in `logs/` directory
- **Logfire dashboard**: Web-based observability (optional)

Enable detailed tracing by setting:

```env
LOGFIRE_TOKEN=your_token_here  # Optional for hosted Logfire
```

---

## 📖 API Documentation

### Orchestration Agent

**Endpoint**: `http://localhost:10024`

**Main Tool**: `create_task(url: str, task: str) -> str`

Example:
```python
result = await a2a_client.create_task(
    "http://localhost:10024", 
    "Find my urgent emails from today"
)
```

### Domain Agents

Each domain agent exposes specialized tools:

- **Gmail Agent** (`http://localhost:10020`): Email search, reading, composition
- **Calendar Agent** (`http://localhost:10023`): Event retrieval, scheduling
- **Todoist Agent** (`http://localhost:10022`): Task management, project operations

Explore the full API at each agent's `/docs` endpoint.

---

## 🤝 Contributing

We welcome contributions! Please:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Contribution Guidelines

- Follow the existing code style (enforced by `ruff`)
- Add tests for new functionality
- Update documentation as needed
- Use conventional commit messages

### Issues and Feature Requests

- **Bug reports**: Use the bug report template
- **Feature requests**: Use the feature request template
- **Questions**: Start a discussion in the repository

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **[Pydantic AI](https://github.com/pydantic/pydantic-ai)** for the powerful agent framework
- **[A2A SDK](https://github.com/pydantic/agent2agent)** for seamless agent communication
- **[Model Context Protocol](https://modelcontextprotocol.io/)** for secure tool integration
- **[Logfire](https://logfire.pydantic.dev/)** for comprehensive observability

---

## 🔗 Related Projects

- [Pydantic AI](https://github.com/pydantic/pydantic-ai) - Type-safe AI agent framework
- [A2A SDK](https://github.com/pydantic/agent2agent) - Agent-to-agent communication
- [MCP Servers](https://github.com/modelcontextprotocol/servers) - Official MCP server implementations
