import { defineStore } from 'pinia'
import { ref } from 'vue'
import { searchRag } from '../api/rag'
import { generate } from '../api/agent'

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
        ? `出处：${data.text_output.source}\n翻译：${data.textOutput?.translation?.slice(0, 60)}…\n分镜：${data.text_output.storyboard?.length || 0} 格`
        : '生成完成'
      chatHistory.value.push({ role: 'assistant', content: summary })
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

  function reset() {
    inputText.value = ''
    ragResults.value = []
    textOutput.value = null
    visualOutput.value = null
    chatHistory.value = []
    followUpText.value = ''
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
    search,
    runGenerate,
    followUp,
    reset,
  }
})
