# ─── Dockerfile ─────────────────────────────────────────────
FROM python:3.12-slim

# Make logs appear immediately
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Where we'll copy the source
WORKDIR /app

# Install build tooling & dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
       build-essential curl nodejs npm && \
    rm -rf /var/lib/apt/lists/*

# Copy source first so that `pip install .` can see it
COPY . /app

# Install the project (this reads pyproject.toml via poetry-core)
RUN pip install --upgrade pip && pip install --no-cache-dir .

# Install npx globally
RUN npm install -g npx

# Listen on each agent port
EXPOSE 10019 10020 10021 10022 10023 8000
# Start the orchestrator that boots every agent
CMD ["python", "app.py"]