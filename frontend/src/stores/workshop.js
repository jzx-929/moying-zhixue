import { defineStore } from 'pinia'
import { ref } from 'vue'
import { searchRag } from '../api/rag'
import { generate } from '../api/agent'
import { saveHistory } from '../api/history'
import { downloadExport } from '../api/export'

export const useWorkshopStore = defineStore('workshop', () => {
  const inputText = ref('')
  const school = ref(null)
  const ragResults = ref([])
  const textOutput = ref(null)
  const visualOutput = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const chatHistory = ref([])
  const followUpText = ref('')
  const lastHistoryId = ref(null)

  async function search() {
    if (!inputText.value.trim()) return
    loading.value = true
    error.value = null
    try {
      const data = await searchRag(inputText.value, 5, school.value)
      ragResults.value = data.items || []
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  async function runGenerate() {
    if (!inputText.value.trim()) return
    loading.value = true
    error.value = null
    try {
      chatHistory.value.push({ role: 'user', content: inputText.value })

      const data = await generate(inputText.value, 'full')
      textOutput.value = data.text_output || null
      visualOutput.value = data.visual_output || null

      const summary = data.text_output
        ? `出处：${data.text_output.source}\n翻译：${data.text_output?.translation?.slice(0, 60)}…\n分镜：${data.text_output.storyboard?.length || 0} 格`
        : '生成完成'
      chatHistory.value.push({ role: 'assistant', content: summary })

      try {
        const histData = await saveHistory({
          title: inputText.value.slice(0, 20),
          input_text: inputText.value,
          output_data: data,
          module: 'workshop',
        })
        lastHistoryId.value = histData.id
      } catch (e) {
        console.error('历史记录保存失败', e)
      }
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  async function followUp() {
    if (!followUpText.value.trim() || !textOutput.value) return
    loading.value = true
    error.value = null

    const userQuestion = followUpText.value
    chatHistory.value.push({ role: 'user', content: userQuestion })

    try {
      const data = await generate(
        `${textOutput.value.source}：${textOutput.value.translation}\n用户追问：${userQuestion}`,
        'text'
      )
      const reply = data.text_output?.translation || data.text_output?.source || '已收到您的追问，正在思考中…'
      chatHistory.value.push({ role: 'assistant', content: reply })

      if (data.text_output?.storyboard) {
        textOutput.value = data.text_output
      }
    } catch (e) {
      const fallback = '抱歉，追问功能需要配置真实 Agent 后才能使用。当前为 Mock 模式。'
      chatHistory.value.push({ role: 'assistant', content: fallback })
    } finally {
      followUpText.value = ''
      loading.value = false
    }
  }

  async function exportResult(format = 'json') {
    if (!textOutput.value) return
    const data = {
      title: inputText.value.slice(0, 20) || '墨影智学作品',
      source: textOutput.value.source || '',
      translation: textOutput.value.translation || '',
      storyboard: textOutput.value.storyboard || [],
      visual_frames: visualOutput.value?.frames || [],
      format,
    }
    const filename = `moying_export.${format}`
    await downloadExport(data, filename)
  }

  function reset() {
    inputText.value = ''
    ragResults.value = []
    textOutput.value = null
    visualOutput.value = null
    chatHistory.value = []
    followUpText.value = ''
    lastHistoryId.value = null
    error.value = null
  }

  return {
    inputText,
    school,
    ragResults,
    textOutput,
    visualOutput,
    loading,
    error,
    chatHistory,
    followUpText,
    lastHistoryId,
    search,
    runGenerate,
    followUp,
    exportResult,
    reset,
  }
})
