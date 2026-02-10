import type { Website, PaginatedResponse, Filters } from '~/types'

export function useWebsites() {
  const { get, getPaginated } = useApi()

  async function fetchWebsites(filters: Filters = {}): Promise<PaginatedResponse<Website>> {
    return getPaginated<Website>('/websites', {
      page: filters.page,
      size: 20,
      category: filters.category,
      style: filters.style,
      collection: filters.collection,
      platform: filters.platform,
      q: filters.q,
    })
  }

  async function fetchWebsite(slug: string): Promise<Website> {
    return get<Website>(`/websites/${slug}`)
  }

  async function fetchFeatured(): Promise<Website[]> {
    return get<Website[]>('/websites/featured')
  }

  async function fetchLatest(): Promise<Website[]> {
    return get<Website[]>('/websites/latest')
  }

  async function fetchPopular(): Promise<Website[]> {
    return get<Website[]>('/websites/popular')
  }

  return {
    fetchWebsites,
    fetchWebsite,
    fetchFeatured,
    fetchLatest,
    fetchPopular,
  }
}
