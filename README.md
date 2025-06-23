# GitHub Helper

![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.13%2B-blue)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

> **GitHub Helper** is an **AI-powered pull-request review service** built with FastAPI & [Pydantic-AI](https://github.com/pydantic/ai).  It plugs directly into your repository through a GitHub Webhook, runs an arsenal of linters, and responds with context-aware review comments, summaries, and risk analyses within minutes.

---

## ✨ Features

1. **Comprehensive AI Code Review** – Multi-phase review agent (analysis → comments → summary) powered by any OpenAI-compatible model.
2. **Automated Lint & Security Scans** – Runs `ruff`, `pylint`, `semgrep`, `gitleaks`, `dotenv-linter`, `markdownlint`, `pytest` and merges the findings into the review.
3. **Incremental Reviews** – Optional agent variant that focuses solely on the diff since the last human review.
4. **PR Overview & Summaries** – Generates a human-friendly overview comment before the detailed review starts.
5. **Interactive Chat** – Converse with the agent directly from PR comments using threads.
6. **Pluggable LLM Provider** – Works with OpenAI, OpenRouter, Anthropic, Google etc. via environment configuration.
7. **Zero-config GitHub Integration** – Just expose one endpoint (`/webhook`) and you are ready to receive reviews.

---

## 📚 Table of Contents

1. [Getting Started](#getting-started)
2. [Project Structure](#project-structure)
3. [Configuration](#configuration)
4. [Local Development](#local-development)
5. [Running in Production](#running-in-production)
6. [GitHub Webhook Setup](#github-webhook-setup)
7. [CLI & Utilities](#cli--utilities)
8. [Contributing](#contributing)
9. [License](#license)

---

## 🚀 Getting Started

### Prerequisites

* Python **3.13+**  (the project uses [PEP-695](https://peps.python.org/pep-0695/) generics)
* GitHub **Personal Access Token** with `repo` scope
* An **OpenAI-compatible** API key (OpenAI, OpenRouter, etc.)

```bash
# Clone the repo
$ git clone https://github.com/your-org/github-helper.git
$ cd github-helper

# Create & activate virtual env
$ python -m venv .venv
$ source .venv/bin/activate           # Windows: .venv\Scripts\activate

# Install runtime deps
$ pip install -e .

# Install dev/CI extras
$ pip install -e .[dev]
```

---

## 🗂️ Project Structure

```text
github-helper/
├── src/
│   ├── app.py                 # FastAPI initialisation & HTTP routes
│   ├── routes/                # Additional REST endpoints
│   ├── agents/
│   │   ├── review_agent/      # Full review agent (multi-phase)
│   │   ├── incr_review_agent/ # Incremental review agent (diff-only)
│   │   └── mr_agent/          # Pull-request summary agent
│   ├── core/                  # Logging, LLM config, linters wrappers
│   └── github/                # Thin MCP client & GitHub helper utilities
├── pyproject.toml             # Poetry-style metadata & deps
├── setup_webhook.sh           # Local tunnelling via smee.io for tests
└── README.md
```

> **Why this layout?** Each concern—agents, GitHub plumbing, infra—is isolated which keeps the review logic testable and easy to evolve.

---

## ⚙️ Configuration

All settings are environment-driven.  Create a `.env` file or export variables in your CI:

```dotenv
# GitHub
GITHUB_TOKEN=ghp_xxx               # required
GITHUB_WEBHOOK_SECRET=xxxxxxxx     # required

# LLM Provider (choose one)
OPENAI_API_KEY=sk-...
# or OPENROUTER_API_KEY=...
REVIEW_AGENT_MODEL=openrouter:gpt-4o-mini

# App
PORT=3000
LOG_LEVEL=INFO
```

> **Tip**: you can switch models at runtime without code changes—great for cost/perf experiments.

---

## 🧑‍💻 Local Development

Run the FastAPI server with hot-reload and an ngrok-like tunnel for GitHub:

```bash
# Starts uvicorn on :3000 with auto-reload
$ uvicorn app:app --reload --port 3000

# In another terminal expose /webhook to the public internet
$ ./setup_webhook.sh  # uses smee.io under the hood
```

Run the (lengthy) linter & test suite locally before pushing:

```bash
$ ruff format . && ruff check .
$ pytest -q
```

---

## 🏗️ Running in Production

There are many ways to deploy – container, serverless function, VM.  A minimal container example:

```dockerfile
# Dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .
COPY ./src ./src
ENV PORT=3000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3000"]
```

Then:

```bash
$ docker build -t github-helper .
$ docker run -d -p 3000:3000 --env-file .env github-helper
```

---

## 🔔 GitHub Webhook Setup

1. Go to **Repository → Settings → Webhooks**.
2. **Add webhook**
   * **Payload URL**: `https://<your-domain>/webhook`
   * **Content type**: `application/json`
   * **Secret**: same as `GITHUB_WEBHOOK_SECRET`
   * **Events**: *Pull requests* & *Pull request reviews*
3. Save — GitHub Helper will now comment automatically on every new PR!

---

## 🛠️ CLI & Utilities

```bash
# Manual trigger (useful for testing)
$ curl -X POST http://localhost:3000/webhook -H "X-GitHub-Event: pull_request" \
       -d @tests/fixtures/pull_request_opened.json

# Inspect agent output with pretty JSON
$ python -m agents.review_agent.debug payload.json
```

---

## 🤝 Contributing

We 💖 contributions!  Feel free to open issues, propose features or send pull requests.

1. Fork → create feature branch (`git checkout -b feat/my-change`)
2. Run `pre-commit install` and make sure `ruff`, `pytest` & `mypy` pass
3. Submit PR & fill out the template — **we use conventional commits**

> **Good first issues** are labelled `help-wanted`.

---

## 📄 License

`github-helper` is released under the [MIT](LICENSE) license.
# personal-asst-a2a
