import api from './index'

export function exportWork(data) {
  return api.post('/export/', data, {
    responseType: 'blob',
    transformResponse: [(data) => data],
  })
}

export function downloadExport(data, filename) {
  return exportWork(data).then((blob) => {
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    a.click()
    URL.revokeObjectURL(url)
  })
}
