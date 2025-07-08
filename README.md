# Personal Assistant A2A

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.13%2B-blue)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

> **Personal Assistant A2A** is a **privacy-first, multi-agent assistant** that connects to your Gmail, Google Calendar and Todoist accounts and answers natural-language questions such as "Do I have any overdue tasks for today?" or "What meetings do I have right after lunch tomorrow?".
>
> Under the hood each capability is implemented by an *agent* that exposes its skills through an HTTP interface using the [A2A SDK](https://github.com/pydantic/agent2agent). A lightweight orchestration agent receives the user prompt, discovers the available agents at runtime and chains their tools to generate the final answer.

---

## ✨ Key Features

1. **Agent-to-Agent Architecture** – Every micro-agent (Gmail, Todoist, Calendar) is a standalone Starlette app that can run locally, remotely or inside a container.
2. **Dynamic Orchestration** – The central *Personal Assistant* agent queries the agent registry, plans a multi-tool workflow and executes it automatically.
3. **Bring-Your-Own-LLM** – Works with any OpenAI-compatible model (OpenAI, Anthropic, Google Vertex, OpenRouter, etc.).
4. **100 % Local Execution** – No data leaves your machine except the calls you intentionally make to the LLM provider.
5. **Extensible** – Write a new agent in ≤ 100 LOC, register it and it will immediately become available to every other agent.

---

## 📚 Table of Contents

1. [Quick Start](#quick-start)
2. [Project Layout](#project-layout)
3. [Configuration](#configuration)
4. [Running the Agents](#running-the-agents)
5. [Adding a New Agent](#adding-a-new-agent)
6. [Development](#development)
7. [Contributing](#contributing)
8. [License](#license)

---

## 🚀 Quick Start

### Prerequisites

* Python **3.13+** (required by `pyproject.toml`)
* An **OpenAI-compatible** API key (e.g. `OPENAI_API_KEY`)
* **Google OAuth 2.0** credentials that allow access to Gmail and Google Calendar *(JSON file)*
* **Todoist** API token *(plain token)*

### Installation

```bash
# 1 – Clone and enter the project
$ git clone https://github.com/your-org/personal-asst-a2a.git
$ cd personal-asst-a2a

# 2 – Create a virtual environment
$ python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3 – Install runtime dependencies
$ pip install -e .
```

Create a `.env` file at the project root (see [Configuration](#configuration)) and drop your `gcp-oauth.keys.json` in the same folder.

Finally start all agents:

```bash
$ python app.py
```

If everything is configured correctly you will see something like:

```
✅ Agent servers are running!
   – Gmail Agent:       http://127.0.0.1:10020
   – Todoist Agent:     http://127.0.0.1:10022
   – Calendar Agent:    http://127.0.0.1:10023
   – Orchestration Agent: http://127.0.0.1:10024
```

The `app.py` bootstrap script will also send an example task to the orchestration agent:

```
>>> has arda@getdelve.com sent me an email today?
```

---

## 🗂️ Project Layout

```text
personal-asst-a2a/
├── app.py                      # Convenience launcher that spins up every agent
├── src/
│   ├── agents/                 # Individual skill agents
│   │   ├── gmail_agent/
│   │   ├── calendar_agent/
│   │   ├── todoist_agent/
│   │   └── orchestration_agent/
│   ├── mcp_handler/            # Thin wrappers around external APIs (Gmail, Todoist, …)
│   ├── core/                   # Shared helpers (logging, subprocess wrapper, linters)
│   └── app.py                  # Turns a Pydantic-AI agent into an A2A server
├── gcp-oauth.keys.json         # Google OAuth credentials (ignored by Git)
├── pyproject.toml              # Build metadata & dependencies
└── README.md
```

---

## ⚙️ Configuration

All settings are **environment variables** consumed by the agents at startup. Create a `.env` file or export them in your shell:

```dotenv
# LLM provider (choose one)
OPENAI_API_KEY=sk-...
# or OPENROUTER_API_KEY=...

# Google services
# Path to the OAuth JSON that contains client_id, client_secret, refresh_token, …
GOOGLE_OAUTH_FILE=gcp-oauth.keys.json

# Todoist
TODOIST_API_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Optional – server ports (default values shown)
PORT_GMAIL=10020
PORT_TODOIST=10022
PORT_CALENDAR=10023
PORT_ORCHESTRATION=10024
```

> **Hint **: The ports can be changed in `app.py`; remember to update the `.env` if you do.

---

## 🏃‍♂️ Running the Agents

The repository ships with a single entry-point that spins up every agent in a background thread and registers them with each other:

```bash
$ python app.py
```

You can also run an agent on its own, e.g. only the Todoist agent:

```bash
$ uvicorn src.agents.todoist_agent.agent:app --port 8080 --reload
```

Each agent serves an **OpenAPI 3** spec at `/docs` and a [JSON schema](https://github.com/pydantic/agent2agent#schema-discovery) at `/.well-known/ai-plugin.json` for automatic discovery by other agents.

---

## ➕ Adding a New Agent

Creating an additional skill agent (e.g. Spotify, Notion, Jira) is straightforward:

1. Create a folder `src/agents/your_agent/`.
2. Implement a Pydantic-AI `Agent` and annotate its tools with `@agent.tool`.
3. Expose the agent as an A2A server:

```python
from pydantic_ai import Agent
from a2a.server.apps import A2AStarletteApplication

agent = Agent(model="openai:gpt-4o-mini", name="spotify_agent")

@agent.tool
def get_recently_played(limit: int = 20):
    ...

app: A2AStarletteApplication = agent.to_a2a()
```

4. Add the server to `app.py` so it launches automatically.

The orchestration agent will pick it up on the next run – no other changes required!

---

## 🧑‍💻 Development

The project follows standard Python best-practices:

```bash
# Format and check style
$ ruff format . && ruff check .

# Run the (placeholder) test suite
$ pytest -q
```

---

## 🤝 Contributing

Contributions are warmly welcomed. Please open an issue or submit a pull request. We use **conventional commits** and automated linting to keep the history clean.

---

## 📄 License

`personal-asst-a2a` is released under the [MIT](LICENSE) license.
