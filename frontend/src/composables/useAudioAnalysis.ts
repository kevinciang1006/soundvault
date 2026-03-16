import { ref } from 'vue'
import axios from 'axios'
import apiClient from '@/api/client'
import { usePostHog } from '@/plugins/posthog'
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
      const { data } = await apiClient.post<AnalysisResult>('/api/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      result.value = data
      usePostHog().capture('audio_analyzed', {
        bpm: data.bpm,
        key: data.key,
        duration_seconds: data.duration_seconds,
        file_name: file.name,
        file_size_bytes: file.size,
      })
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
