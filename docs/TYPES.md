# Shared Types

## Website
```typescript
interface Website {
  id: number
  slug: string
  title: string
  description: string | null
  original_url: string | null
  thumbnail_url: string | null
  image_url: string | null
  is_featured: boolean
  view_count: number
  created_at: string
  updated_at: string
  categories: CategoryBrief[]
  styles: StyleBrief[]
  collections: CollectionBrief[]
  platform: PlatformBrief | null
}

interface WebsiteListItem {
  id: number
  slug: string
  title: string
  description: string | null
  original_url: string | null
  thumbnail_url: string | null
  is_featured: boolean
  view_count: number
  created_at: string
  categories: CategoryBrief[]
}
```

## Category
```typescript
interface CategoryBrief {
  id: number
  slug: string
  title: string
}

interface Category extends CategoryBrief {
  description: string | null
  icon: string | null
  website_count: number
  is_active: boolean
}
```

## Style
```typescript
interface StyleBrief {
  id: number
  slug: string
  title: string
}

interface Style extends StyleBrief {
  website_count: number
  is_active: boolean
}
```

## Collection
```typescript
interface CollectionBrief {
  id: number
  slug: string
  title: string
}

interface Collection extends CollectionBrief {
  description: string | null
  website_count: number
  is_active: boolean
}
```

## Platform
```typescript
interface PlatformBrief {
  id: number
  slug: string
  title: string
}

interface Platform extends PlatformBrief {
  website_url: string | null
  website_count: number
  is_active: boolean
}
```

## API Response
```typescript
interface PaginationMeta {
  page: number
  per_page: number
  total: number
  total_pages: number
}

interface PaginatedResponse<T> {
  data: T[]
  meta: PaginationMeta
}

interface Filters {
  category?: string
  style?: string
  collection?: string
  platform?: string
  featured?: boolean
  q?: string
  page?: number
  per_page?: number
  sort_by?: string
  sort_order?: 'asc' | 'desc'
}
```
