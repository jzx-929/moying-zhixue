import api from './index'

export function recognizeImage(file, doGenerate = false) {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('do_generate', doGenerate)
  return api.post('/ocr/recognize', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export function generateFromImage(file) {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/ocr/generate-from-image', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}
