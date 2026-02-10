# UILove API Documentation

## Base URL
```
Development: http://localhost:8000/api/v1
```

## Authentication
JWT Bearer token for admin routes.
```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@uilove.co", "password": "changeme123"}'

# Use token
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer <token>"
```

## Endpoints

### Websites

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /websites | No | List websites |
| GET | /websites/{slug} | No | Get single website |
| GET | /websites/featured | No | Featured websites |
| GET | /websites/latest | No | Latest websites |
| GET | /websites/popular | No | Most viewed |
| POST | /websites | Yes | Create website |
| PUT | /websites/{slug} | Yes | Update website |
| DELETE | /websites/{slug} | Yes | Delete website |

### Query Parameters
```
?page=1           # Page number
&per_page=20      # Items per page (max 100)
&category=minimal # Filter by category slug
&style=dark-mode  # Filter by style slug
&collection=gsap  # Filter by collection slug
&platform=webflow # Filter by platform slug
&featured=true    # Featured only
&q=search         # Search query
&sort_by=created_at  # Sort field
&sort_order=desc     # asc or desc
```

### Categories
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /categories | All categories |
| GET | /categories/{slug} | Single category |
| GET | /categories/{slug}/websites | Websites in category |

### Styles
| GET | /styles | All styles |
| GET | /styles/{slug}/websites | Websites by style |

### Collections
| GET | /collections | All collections |
| GET | /collections/{slug}/websites | Websites by collection |

### Platforms
| GET | /platforms | All platforms |
| GET | /platforms/{slug}/websites | Websites by platform |

### Search
| GET | /search?q=term | Full-text search |

## Response Format

### List Response
```json
{
  "data": [
    {
      "id": 1,
      "slug": "example-site",
      "title": "Example Site",
      "description": "Description here",
      "original_url": "https://example.com",
      "thumbnail_url": "https://cdn.example.com/thumb.webp",
      "image_url": "https://cdn.example.com/image.webp",
      "is_featured": false,
      "view_count": 150,
      "created_at": "2024-01-15T10:30:00Z",
      "categories": [
        {"id": 1, "slug": "minimal", "title": "Minimal"}
      ]
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

### Single Response
```json
{
  "id": 1,
  "slug": "example-site",
  "title": "Example Site",
  "description": "Full description",
  "original_url": "https://example.com",
  "thumbnail_url": "https://cdn.example.com/thumb.webp",
  "image_url": "https://cdn.example.com/image.webp",
  "is_featured": false,
  "view_count": 150,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "categories": [...],
  "styles": [...],
  "collections": [...],
  "platform": {"id": 1, "slug": "webflow", "title": "Webflow"}
}
```

### Error Response
```json
{
  "detail": "Error message here"
}
```
