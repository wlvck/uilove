# UILove Backend

> Main docs: ../../CLAUDE.md

## Status: ✅ Complete

## Commands (run from this folder)
```bash
docker-compose up -d
uv run uvicorn app.main:app --reload
uv run alembic upgrade head
uv run python -m scripts.import_data --all
```
