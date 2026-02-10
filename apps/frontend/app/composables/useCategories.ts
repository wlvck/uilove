import type { Category, Style, Collection, Platform, Website, PaginatedResponse } from '~/types'

export function useCategories() {
  const { get, getPaginated } = useApi()

  async function fetchCategories(): Promise<Category[]> {
    return get<Category[]>('/categories')
  }

  async function fetchCategoryWebsites(slug: string, page = 1): Promise<PaginatedResponse<Website>> {
    return getPaginated<Website>(`/categories/${slug}/websites`, { page })
  }

  async function fetchStyles(): Promise<Style[]> {
    return get<Style[]>('/styles')
  }

  async function fetchStyleWebsites(slug: string, page = 1): Promise<PaginatedResponse<Website>> {
    return getPaginated<Website>(`/styles/${slug}/websites`, { page })
  }

  async function fetchCollections(): Promise<Collection[]> {
    return get<Collection[]>('/collections')
  }

  async function fetchCollectionWebsites(slug: string, page = 1): Promise<PaginatedResponse<Website>> {
    return getPaginated<Website>(`/collections/${slug}/websites`, { page })
  }

  async function fetchPlatforms(): Promise<Platform[]> {
    return get<Platform[]>('/platforms')
  }

  return {
    fetchCategories,
    fetchCategoryWebsites,
    fetchStyles,
    fetchStyleWebsites,
    fetchCollections,
    fetchCollectionWebsites,
    fetchPlatforms,
  }
}
