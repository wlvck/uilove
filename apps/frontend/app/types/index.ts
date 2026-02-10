export interface CategoryBrief {
  id: number
  slug: string
  title: string
}

export interface StyleBrief {
  id: number
  slug: string
  title: string
}

export interface CollectionBrief {
  id: number
  slug: string
  title: string
}

export interface PlatformBrief {
  id: number
  slug: string
  title: string
}

export interface Website {
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
  // These fields are only present in detail view (WebsiteRead), not in list view (WebsiteListItem)
  categories?: CategoryBrief[]
  styles?: StyleBrief[]
  collections?: CollectionBrief[]
  platform?: PlatformBrief | null
}

export interface Category extends CategoryBrief {
  description: string | null
  icon: string | null
  website_count: number
}

export interface Style extends StyleBrief {
  description: string | null
  website_count: number
}

export interface Collection extends CollectionBrief {
  description: string | null
  website_count: number
}

export interface Platform extends PlatformBrief {
  description: string | null
  website_count: number
}

export interface PaginationMeta {
  page: number
  size: number
  total: number
  pages: number
}

export interface PaginatedResponse<T> {
  items: T[]
  page: number
  size: number
  total: number
  pages: number
}

export interface Filters {
  category?: string
  style?: string
  collection?: string
  platform?: string
  q?: string
  page?: number
}

// Admin types

export interface User {
  id: number
  email: string
  full_name: string | null
  is_superuser: boolean
  is_active: boolean
  created_at: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface Token {
  access_token: string
  token_type: string
}

export interface WebsiteCreate {
  title: string
  slug: string
  description?: string | null
  original_url?: string | null
  thumbnail_url?: string | null
  image_url?: string | null
  is_featured?: boolean
  platform_id?: number | null
  category_ids?: number[]
  style_ids?: number[]
  collection_ids?: number[]
}

export interface WebsiteUpdate {
  title?: string | null
  description?: string | null
  original_url?: string | null
  thumbnail_url?: string | null
  image_url?: string | null
  platform_id?: number | null
  is_featured?: boolean | null
  is_active?: boolean | null
  category_ids?: number[] | null
  style_ids?: number[] | null
  collection_ids?: number[] | null
}
