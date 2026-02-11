# UILove Backend

> Main docs: ../../CLAUDE.md

## Status: ✅ Complete

## Commands (run from this folder)
```bash
# Start databases (from project root)
docker compose -f ../../docker-compose.dev.yml up -d

# Run server
uv run uvicorn app.main:app --reload

# Migrations
uv run alembic upgrade head

# Tests
uv run pytest

# Import data
uv run python -m scripts.import_data --all
```
