import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface SearchRequest {
  keyword: string
  num_results: number
  start_year?: number
  end_year?: number
  sort_by: string
}

export interface Article {
  id?: number
  title: string
  authors?: string
  venue?: string
  publisher?: string
  year?: number
  citations: number
  citations_per_year: number
  description?: string
  url?: string
  created_at?: string
}

export interface SearchResponse {
  search_id: number
  keyword: string
  total_results: number
  articles: Article[]
  message: string
}

export interface Search {
  id: number
  keyword: string
  start_year?: number
  end_year?: number
  total_results: number
  created_at: string
  articles?: Article[]
}


export const searchAPI = {
  search: async (params: SearchRequest): Promise<SearchResponse> => {
    const { data } = await api.post<SearchResponse>('/search', params)
    return data
  },

  getSearchHistory: async (skip = 0, limit = 20): Promise<Search[]> => {
    const { data } = await api.get<Search[]>('/searches', { params: { skip, limit } })
    return data
  },

  getSearchDetails: async (searchId: number): Promise<Search> => {
    const { data } = await api.get<Search>(`/search/${searchId}`)
    return data
  },

  deleteSearch: async (searchId: number): Promise<void> => {
    await api.delete(`/search/${searchId}`)
  },

  exportResults: async (searchId: number, format: string): Promise<Blob> => {
    const { data } = await api.get(`/export/${searchId}`, {
      params: { format },
      responseType: 'blob',
    })
    return data
  },
}


export default api