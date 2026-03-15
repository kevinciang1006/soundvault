import { ref } from 'vue'
import axios from 'axios'
import type { AnalysisResult } from '@/types'

export function useAudioAnalysis() {
  const result = ref<AnalysisResult | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  async function analyzeFile(file: File) {
    isLoading.value = true
    error.value = null
    result.value = null

    const formData = new FormData()
    formData.append('file', file)

    try {
      const { data } = await axios.post<AnalysisResult>('/api/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      result.value = data
    } catch (err: unknown) {
      if (axios.isAxiosError(err)) {
        error.value = err.response?.data?.detail ?? 'Analysis failed. Please try again.'
      } else {
        error.value = 'An unexpected error occurred.'
      }
    } finally {
      isLoading.value = false
    }
  }

  return {
    result,
    isLoading,
    error,
    analyzeFile,
  }
}
