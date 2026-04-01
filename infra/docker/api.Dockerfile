# Edvance API — for Phase 1 VPS deployment (also used for local dev)
FROM python:3.12-slim

WORKDIR /app

# System deps for asyncpg + weasyprint
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc libcairo2 libpango-1.0-0 libpangocairo-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy workspace files
COPY pyproject.toml uv.lock ./
COPY shared/ ./shared/
COPY api/ ./api/

# Install dependencies
RUN uv sync --no-dev --frozen

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "api.main:app", \
     "--host", "0.0.0.0", "--port", "8000", \
     "--workers", "4", "--loop", "uvloop"]
