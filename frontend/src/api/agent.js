import api from './index'

export function generate(text, mode = 'full') {
  return api.post('/agent/generate', { text, mode })
}
