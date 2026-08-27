import api from './index'

export function searchRag(query, topK = 5, school = null) {
  return api.get('/rag/search', { params: { q: query, top_k: topK, school } })
}

export function getRagInfo() {
  return api.get('/rag/info')
}
