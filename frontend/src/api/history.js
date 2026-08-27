import api from './index'

export function saveHistory(data) {
  return api.post('/history/', data)
}

export function listHistory(module, limit = 20) {
  return api.get('/history/', { params: { module, limit } })
}

export function getHistory(id) {
  return api.get(`/history/${id}`)
}

export function deleteHistory(id) {
  return api.delete(`/history/${id}`)
}
