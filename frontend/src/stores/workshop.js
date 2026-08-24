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
      const data = await generate(inputText.value, 'full')
      textOutput.value = data.text_output || null
      visualOutput.value = data.visual_output || null
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  function reset() {
    inputText.value = ''
    ragResults.value = []
    textOutput.value = null
    visualOutput.value = null
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
    search,
    runGenerate,
    reset,
  }
})
