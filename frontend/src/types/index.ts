export interface Pack {
  id: number
  name: string
  creator: string
  genre: string
  sample_count: number
  cover_color: string
  cover_color_2: string
}

export interface Sample {
  id: number
  pack_id: number
  pack_name: string
  pack_creator: string
  filename: string
  genre: string
  sample_type: 'loop' | 'one_shot' | 'vocal' | 'fx'
  bpm: number
  key: string
  duration_seconds: number
  is_premium: boolean
  play_count: number
}

export interface AnalysisResult {
  bpm: number
  key: string
  duration_seconds: number
  filename: string
}

export interface SampleFilters {
  q: string
  genre: string
  bpm_min: number
  bpm_max: number
  key: string
  sample_type: string
  pack_id: number | null
  sort: 'trending' | 'newest' | 'bpm_asc' | 'bpm_desc'
}
