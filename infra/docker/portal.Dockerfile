# Edvance Portal — Django + HTMX
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc libcairo2 libpango-1.0-0 libpangocairo-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
COPY shared/ ./shared/
COPY portal/ ./portal/

RUN uv sync --no-dev --frozen

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=portal.core.settings.production

RUN uv run python portal/manage.py collectstatic --noinput

EXPOSE 8080

CMD ["uv", "run", "gunicorn", "portal.core.wsgi:application", \
     "--bind", "0.0.0.0:8080", "--workers", "4", "--timeout", "120"]
