# UILove

A curated gallery of beautifully designed landing pages with animations.

## Overview

UILove is a full-stack web application that showcases a collection of stunning landing pages. Users can browse, search, and filter websites by categories, styles, and more. The platform features smooth animations and a modern, responsive design.

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy 2.0** - Async ORM
- **PostgreSQL 16** - Primary database
- **Redis 7** - Caching layer
- **JWT** - Authentication
- **Alembic** - Database migrations

### Frontend
- **Nuxt 4** - Vue.js meta-framework
- **Tailwind CSS** - Utility-first CSS
- **Radix Vue** - Accessible UI components
- **GSAP + Lenis** - Smooth animations
- **Pinia** - State management
- **VueUse** - Vue composition utilities

## Project Structure

```
uilove/
├── apps/
│   ├── backend/          # FastAPI API server
│   │   ├── app/
│   │   │   ├── api/      # API routes
│   │   │   ├── core/     # Config, security, cache
│   │   │   ├── crud/     # Database operations
│   │   │   ├── models/   # SQLAlchemy models
│   │   │   └── schemas/  # Pydantic schemas
│   │   ├── alembic/      # Database migrations
│   │   ├── data/         # Seed data (JSON/CSV)
│   │   └── scripts/      # Import scripts
│   │
│   └── frontend/         # Nuxt 4 application
│       ├── app/
│       │   ├── components/
│       │   ├── composables/
│       │   ├── layouts/
│       │   ├── pages/
│       │   └── stores/
│       ├── public/
│       └── tests/
│
├── parser/               # Data scraping tools
│   ├── parse_categories.py
│   ├── scrape_landing_love.py
│   └── requirements.txt
├── docs/                 # Documentation
├── docker-compose.yml    # Full stack deployment
└── docker-compose.dev.yml # Development databases
```

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 22+ (for local frontend development)
- Python 3.13+ with uv (for local backend development)

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/uilove.git
cd uilove

# Start all services
docker compose up -d

# Import seed data
docker exec uilove-db psql -U uilove -d uilove -c "CREATE EXTENSION IF NOT EXISTS pg_trgm;"
docker exec uilove-backend mkdir -p /app/data
docker cp apps/backend/data/. uilove-backend:/app/data/
docker exec uilove-backend uv run python -m scripts.import_data --all

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Development

```bash
# Start databases only
docker compose -f docker-compose.dev.yml up -d

# Terminal 1: Backend
cd apps/backend
cp .env.example .env
uv run alembic upgrade head
uv run python -m scripts.import_data --all
uv run uvicorn app.main:app --reload

# Terminal 2: Frontend
cd apps/frontend
yarn install
yarn dev
```

## API Reference

Base URL: `http://localhost:8000/api/v1`

### Websites

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/websites` | List websites (paginated) |
| GET | `/websites/{slug}` | Get website by slug |
| GET | `/websites/featured` | Featured websites |
| GET | `/websites/latest` | Latest websites |
| GET | `/websites/popular` | Most viewed websites |

**Query Parameters for `/websites`:**
- `page` - Page number (default: 1)
- `size` - Items per page (default: 20, max: 100)
- `category` - Filter by category slug
- `style` - Filter by style slug

### Categories & Filters

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/categories` | All categories |
| GET | `/categories/{slug}/websites` | Websites in category |
| GET | `/styles` | All styles |
| GET | `/collections` | All collections |
| GET | `/platforms` | All platforms |
| GET | `/search?q=` | Full-text search |

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | Get JWT token |
| GET | `/auth/me` | Current user info |

### Admin Endpoints (Requires Auth)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/websites` | Create website |
| PUT | `/websites/{slug}` | Update website |
| DELETE | `/websites/{slug}` | Delete website |

## Development

### Backend Commands

```bash
cd apps/backend

# Run development server
uv run uvicorn app.main:app --reload

# Run migrations
uv run alembic upgrade head
uv run alembic revision --autogenerate -m "description"

# Run tests
uv run pytest

# Import data
uv run python -m scripts.import_data --all
uv run python -m scripts.import_data --categories
uv run python -m scripts.import_data --websites
uv run python -m scripts.import_data --admin
```

### Frontend Commands

```bash
cd apps/frontend

# Development
yarn dev

# Build for production
yarn build

# Preview production build
yarn preview

# Type checking
yarn typecheck

# Run tests
yarn test              # Unit tests (watch mode)
yarn test:unit         # Unit tests (single run)
yarn test:e2e          # E2E tests
yarn test:e2e:ui       # E2E tests with UI
```

### Docker Commands

```bash
# Full stack
docker compose up -d              # Start all services
docker compose down               # Stop all services
docker compose logs -f            # View logs
docker compose up -d --build      # Rebuild and start

# Development (databases only)
docker compose -f docker-compose.dev.yml up -d
docker compose -f docker-compose.dev.yml down
```

## Environment Variables

### Backend (`apps/backend/.env`)

```env
APP_ENV=development
DEBUG=true
DATABASE_URL=postgresql+asyncpg://uilove:password@localhost:5432/uilove
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-super-secret-key
ADMIN_EMAIL=admin@uilove.co
ADMIN_PASSWORD=changeme123
CORS_ORIGINS=http://localhost:3000
```

### Frontend (`apps/frontend/.env`)

```env
NUXT_PUBLIC_API_BASE=http://localhost:8000/api/v1
```

## Testing

### Unit Tests (Frontend)

```bash
cd apps/frontend
yarn test:unit
```

Tests cover UI components including Button, Badge, Input, and LoadingSpinner.

### E2E Tests (Frontend)

```bash
cd apps/frontend
yarn test:e2e:install  # Install Playwright browsers
yarn test:e2e          # Run E2E tests
```

E2E tests cover:
- Home page
- Search functionality
- Categories navigation
- Admin authentication

### Backend Tests

```bash
cd apps/backend
uv run pytest
```

## Data Parser

The `parser/` directory contains web scraping tools to collect landing page data from [landing.love](https://landing.love).

### Parser Structure

```
parser/
├── parse_categories.py      # Extract categories, styles, collections
├── scrape_landing_love.py   # Main scraper for websites
├── requirements.txt         # Python dependencies
├── categories.json          # Output: category definitions
└── websites_complete.csv    # Output: all website data
```

### Setup

```bash
cd parser
pip install -r requirements.txt
```

**Dependencies:**
- `requests` - HTTP client
- `beautifulsoup4` - HTML parsing
- `lxml` - Fast XML/HTML parser

### Usage

#### Step 1: Parse Categories

```bash
python parse_categories.py
```

**Output:** `categories.json`
```json
[
  {
    "title": "Minimal",
    "url": "https://www.landing.love/categories/minimal/",
    "count": 1298,
    "slug": "minimal"
  }
]
```

#### Step 2: Scrape All Websites

```bash
python scrape_landing_love.py
```

This script runs in two phases:

**Phase 1:** Crawls all category pages to collect website listings
- Iterates through all categories
- Handles pagination automatically
- Deduplicates websites across categories

**Phase 2:** Fetches detailed information for each website
- Description from meta tags
- Original website URL
- Tags and categories
- Progress saved automatically (safe to interrupt)

**Output Files:**
- `websites_basic.json` - Basic info (after Phase 1)
- `websites_progress.json` - Progress file (during Phase 2)
- `websites_complete.json` - Full data (final)
- `websites_complete.csv` - CSV format for easy viewing

### Output Data Structure

```json
{
  "slug": "example-site",
  "title": "Example Site",
  "description": "A beautiful landing page...",
  "original_url": "https://example.com",
  "thumbnail": "https://cdn.landing.love/images/example-site-thumb.webp",
  "image_url": "https://cdn.landing.love/images/example-site.webp",
  "video_url": "https://cdn.landing.love/videos/example-site.mp4",
  "detail_url": "https://www.landing.love/sites/example-site/",
  "categories": ["minimal", "portfolio"],
  "tags": ["Minimal", "Dark Mode", "GSAP"]
}
```

### Refreshing Data

To update the database with fresh scraped data:

```bash
# 1. Run the scraper
cd parser
python scrape_landing_love.py

# 2. Copy output to backend data folder
cp categories.json websites_complete.csv ../apps/backend/data/

# 3. Re-import into database
cd ../apps/backend
uv run python -m scripts.import_data --all
```

### Rate Limiting

The scraper includes built-in politeness features:
- 1-2 second delays between requests
- Automatic retry with exponential backoff
- Progress saving every 20 websites

## License

This project is licensed under the MIT License.
