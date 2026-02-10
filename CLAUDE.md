# UILove - Monorepo

A curated gallery of beautifully designed landing pages with animations.

## Project Structure

```
uilove/
├── apps/
│   ├── backend/       # FastAPI (Python)
│   └── frontend/      # Nuxt 4 (Vue)
├── docs/              # Shared documentation
└── CLAUDE.md          # This file
```

## Tech Stack

### Backend (apps/backend)

- FastAPI + Uvicorn
- SQLAlchemy 2.0 (async)
- PostgreSQL 16 + Redis 7 (Docker)
- JWT Auth
- Status: ✅ Complete

### Frontend (apps/frontend)

- Nuxt 4
- Tailwind CSS + tailwind-animate
- Radix Vue
- GSAP + Lenis (animations)
- Pinia + VueUse
- Status: 🚧 In Progress

## Quick Start

```bash
# 1. Start databases
cd apps/backend
docker-compose up -d

# 2. Run backend (terminal 1)
cd apps/backend
uv run uvicorn app.main:app --reload
# API: http://localhost:8000
# Docs: http://localhost:8000/docs

# 3. Run frontend (terminal 2)
cd apps/frontend
yarn dev
# App: http://localhost:3000
```

## API Endpoints

Base: http://localhost:8000/api/v1

| Method | Endpoint                    | Description                  |
| ------ | --------------------------- | ---------------------------- |
| GET    | /websites                   | List (paginated, filterable) |
| GET    | /websites/{slug}            | Single website detail        |
| GET    | /websites/featured          | Featured websites            |
| GET    | /websites/latest            | Latest websites              |
| GET    | /websites/popular           | Most viewed                  |
| GET    | /categories                 | All categories               |
| GET    | /categories/{slug}/websites | Websites in category         |
| GET    | /styles                     | All styles                   |
| GET    | /collections                | All collections              |
| GET    | /platforms                  | All platforms                |
| GET    | /search?q=                  | Full-text search             |

### Query Params (for /websites)

```
?page=1
&per_page=20
&category=minimal
&style=dark-mode
&collection=gsap
&platform=webflow
&featured=true
&q=search+term
```

### Response Format

```json
{
  "data": [...],
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

## Types (shared)

```typescript
interface Website {
  id: number;
  slug: string;
  title: string;
  description: string | null;
  original_url: string | null;
  thumbnail_url: string | null;
  image_url: string | null;
  is_featured: boolean;
  view_count: number;
  created_at: string;
  categories: CategoryBrief[];
  styles: StyleBrief[];
  collections: CollectionBrief[];
  platform: PlatformBrief | null;
}

interface CategoryBrief {
  id: number;
  slug: string;
  title: string;
}

interface Category extends CategoryBrief {
  description: string | null;
  website_count: number;
}

interface Style {
  id: number;
  slug: string;
  title: string;
  website_count: number;
}

interface Collection {
  id: number;
  slug: string;
  title: string;
  description: string | null;
  website_count: number;
}

interface Platform {
  id: number;
  slug: string;
  title: string;
  website_count: number;
}

interface PaginatedResponse<T> {
  data: T[];
  meta: {
    page: number;
    per_page: number;
    total: number;
    total_pages: number;
  };
}

interface Filters {
  category?: string;
  style?: string;
  collection?: string;
  platform?: string;
  q?: string;
  page?: number;
  per_page?: number;
}
```

## Current Status

### Backend ✅

- [x] All models & migrations
- [x] All API endpoints
- [x] JWT auth
- [x] Redis caching
- [x] Full-text search
- [x] Data import script

### Frontend 🚧

- [x] Project setup
- [x] Dependencies installed
- [ ] nuxt.config.ts
- [ ] Tailwind config
- [ ] Types
- [ ] API composables
- [ ] Pinia stores
- [ ] Layout (Header, Footer)
- [ ] Components (WebsiteCard, WebsiteGrid)
- [ ] Pages (Home, Detail, Category, Search)
- [ ] Animations (GSAP + Lenis)

## Working Guidelines

1. **Backend changes**: cd apps/backend
2. **Frontend changes**: cd apps/frontend
3. **Commit often**: After each feature
4. **Test locally**: Both services running

## Commands Reference

### Backend

```bash
cd apps/backend
docker-compose up -d          # Start DB
uv run uvicorn app.main:app --reload  # Run server
uv run alembic upgrade head   # Migrations
uv run python -m scripts.import_data --all  # Import data
```

### Frontend

```bash
cd apps/frontend
yarn dev          # Dev server
yarn build        # Production build
yarn preview      # Preview build
```

## Documentation
- docs/API.md - API endpoints reference
- docs/TYPES.md - Shared TypeScript types
- docs/openapi.json - OpenAPI spec (auto-generated)
