import { ref, reactive, watch } from 'vue'
import axios from 'axios'
import type { Sample, Pack, SampleFilters } from '@/types'

export function useSamples() {
  const samples = ref<Sample[]>([])
  const packs = ref<Pack[]>([])
  const total = ref(0)
  const isLoading = ref(false)

  const filters = reactive<SampleFilters>({
    q: '',
    genre: '',
    bpm_min: 60,
    bpm_max: 200,
    key: '',
    sample_type: '',
    pack_id: null,
    sort: 'trending',
  })

  let debounceTimer: ReturnType<typeof setTimeout> | null = null

  async function fetchSamples(offset = 0) {
    isLoading.value = true
    try {
      const params: Record<string, string | number> = {
        limit: 20,
        offset,
        sort: filters.sort,
      }

      if (filters.q) params.q = filters.q
      if (filters.genre) params.genre = filters.genre
      if (filters.bpm_min > 60) params.bpm_min = filters.bpm_min
      if (filters.bpm_max < 200) params.bpm_max = filters.bpm_max
      if (filters.key) params.key = filters.key
      if (filters.sample_type) params.sample_type = filters.sample_type
      if (filters.pack_id !== null) params.pack_id = filters.pack_id

      const { data } = await axios.get('/api/samples', { params })
      if (offset === 0) {
        samples.value = data.samples
      } else {
        samples.value = [...samples.value, ...data.samples]
      }
      total.value = data.total
    } catch (err) {
      console.error('Failed to fetch samples:', err)
    } finally {
      isLoading.value = false
    }
  }

  async function fetchPacks() {
    try {
      const { data } = await axios.get('/api/packs')
      packs.value = data
    } catch (err) {
      console.error('Failed to fetch packs:', err)
    }
  }

  function resetFilters() {
    filters.q = ''
    filters.genre = ''
    filters.bpm_min = 60
    filters.bpm_max = 200
    filters.key = ''
    filters.sample_type = ''
    filters.pack_id = null
    filters.sort = 'trending'
  }

  watch(
    filters,
    () => {
      if (debounceTimer) clearTimeout(debounceTimer)
      debounceTimer = setTimeout(() => {
        fetchSamples(0)
      }, 300)
    },
    { deep: true }
  )

  return {
    samples,
    packs,
    total,
    isLoading,
    filters,
    fetchSamples,
    fetchPacks,
    resetFilters,
  }
}
