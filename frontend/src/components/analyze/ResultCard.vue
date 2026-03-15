<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import type { AnalysisResult } from '@/types'

const props = defineProps<{
  result: AnalysisResult
}>()

const emit = defineEmits<{
  (e: 'reset'): void
}>()

const router = useRouter()

const formattedDuration = computed(() => {
  const total = Math.round(props.result.duration_seconds)
  const m = Math.floor(total / 60)
  const s = total % 60
  return `${m}:${s.toString().padStart(2, '0')}`
})

const isMinor = computed(() => props.result.key.endsWith('m'))
const rootNote = computed(() => props.result.key.replace('m', ''))

function browseSoundsInKey() {
  router.push({ path: '/sounds', query: { key: props.result.key } })
}
</script>

<template>
  <div class="bg-surface border border-border rounded-2xl p-8 text-center">
    <!-- Filename -->
    <p class="font-mono text-sm text-text-muted mb-6 truncate">{{ result.filename }}</p>

    <!-- BPM -->
    <div class="mb-6">
      <p class="text-xs font-sans font-semibold text-text-muted uppercase tracking-widest mb-2">Tempo</p>
      <div class="font-serif text-7xl text-text-primary leading-none">
        {{ result.bpm }}
      </div>
      <p class="text-lg font-sans text-text-muted mt-1">BPM</p>
    </div>

    <!-- Key + Duration row -->
    <div class="flex items-center justify-center gap-8 mb-8">
      <div>
        <p class="text-xs font-sans font-semibold text-text-muted uppercase tracking-widest mb-2">Key</p>
        <div class="flex items-center gap-2">
          <span class="font-serif text-3xl text-text-primary">{{ rootNote }}</span>
          <span
            class="px-2 py-0.5 rounded-full text-xs font-sans font-semibold"
            :class="isMinor ? 'bg-primary/20 text-primary' : 'bg-accent/20 text-accent'"
          >
            {{ isMinor ? 'Minor' : 'Major' }}
          </span>
        </div>
      </div>

      <div class="w-px h-10 bg-border" />

      <div>
        <p class="text-xs font-sans font-semibold text-text-muted uppercase tracking-widest mb-2">Duration</p>
        <span class="font-mono text-2xl text-text-primary">{{ formattedDuration }}</span>
      </div>
    </div>

    <!-- Actions -->
    <div class="flex flex-col sm:flex-row gap-3">
      <button
        class="flex-1 px-4 py-3 bg-primary hover:bg-primary/90 text-white font-sans font-semibold text-sm rounded-xl transition-colors duration-200"
        @click="browseSoundsInKey"
      >
        Find samples in {{ result.key }} &rarr;
      </button>
      <button
        class="flex-1 px-4 py-3 border border-border text-text-secondary hover:border-primary hover:text-text-primary font-sans font-medium text-sm rounded-xl transition-all duration-200"
        @click="emit('reset')"
      >
        Analyze another
      </button>
    </div>
  </div>
</template>
