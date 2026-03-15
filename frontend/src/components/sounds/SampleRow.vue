<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Sample } from '@/types'
import WaveformBar from './WaveformBar.vue'

const props = defineProps<{
  sample: Sample
  isPlaying: boolean
  isCurrentSample: boolean
}>()

const emit = defineEmits<{
  (e: 'play', sample: Sample): void
}>()

const isLiked = ref(false)
const isHovered = ref(false)

const formattedDuration = computed(() => {
  const total = Math.round(props.sample.duration_seconds)
  const m = Math.floor(total / 60)
  const s = total % 60
  return `${m}:${s.toString().padStart(2, '0')}`
})

const typeColors: Record<string, string> = {
  loop: 'bg-primary/20 text-primary',
  one_shot: 'bg-accent/20 text-accent',
  vocal: 'bg-pink-500/20 text-pink-400',
  fx: 'bg-yellow-500/20 text-yellow-400',
}
</script>

<template>
  <div
    class="relative flex items-center gap-4 px-4 py-3 rounded-lg transition-all duration-200 cursor-default group"
    :class="[
      isCurrentSample ? 'bg-surface-raised' : 'hover:bg-surface-raised',
    ]"
    :style="isCurrentSample ? 'border-left: 3px solid #6366f1; padding-left: 13px;' : 'border-left: 3px solid transparent;'"
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
  >
    <!-- Play / Waveform column -->
    <div class="flex-shrink-0 w-8 flex items-center justify-center">
      <WaveformBar v-if="isCurrentSample" :is-playing="isPlaying" />
      <button
        v-else
        class="opacity-0 group-hover:opacity-100 transition-opacity duration-200 w-7 h-7 rounded-full bg-primary/20 hover:bg-primary flex items-center justify-center text-primary hover:text-white"
        @click="emit('play', sample)"
      >
        <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
          <path d="M8 5v14l11-7z"/>
        </svg>
      </button>
    </div>

    <!-- Filename + pack -->
    <div class="flex-1 min-w-0">
      <p class="font-mono text-sm text-text-primary truncate">{{ sample.filename }}</p>
      <p class="text-xs font-sans text-text-muted truncate">{{ sample.pack_name }}</p>
    </div>

    <!-- Badges -->
    <div class="hidden sm:flex items-center gap-2 flex-shrink-0">
      <span class="px-1.5 py-0.5 bg-accent/20 text-accent font-mono text-xs rounded">
        {{ sample.bpm }} BPM
      </span>
      <span class="px-1.5 py-0.5 bg-primary/20 text-primary font-mono text-xs rounded">
        {{ sample.key }}
      </span>
      <span
        class="px-1.5 py-0.5 font-sans text-xs rounded capitalize"
        :class="typeColors[sample.sample_type] ?? 'bg-surface-raised text-text-muted'"
      >
        {{ sample.sample_type.replace('_', ' ') }}
      </span>
    </div>

    <!-- Duration -->
    <div class="hidden md:block flex-shrink-0 text-xs font-sans text-text-muted w-10 text-right">
      {{ formattedDuration }}
    </div>

    <!-- Actions -->
    <div class="flex-shrink-0 flex items-center gap-2">
      <button
        class="w-7 h-7 flex items-center justify-center rounded-lg transition-colors duration-200"
        :class="isLiked ? 'text-red-500' : 'text-text-muted hover:text-red-400'"
        @click="isLiked = !isLiked"
        :aria-label="isLiked ? 'Unlike' : 'Like'"
      >
        <svg width="14" height="14" viewBox="0 0 24 24" :fill="isLiked ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2">
          <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
        </svg>
      </button>

      <button
        class="w-7 h-7 flex items-center justify-center rounded-lg transition-colors duration-200"
        :class="sample.is_premium ? 'text-text-muted cursor-not-allowed' : 'text-text-muted hover:text-text-primary'"
        :title="sample.is_premium ? 'Premium — upgrade to download' : 'Download'"
      >
        <svg v-if="sample.is_premium" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
          <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
        </svg>
        <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
          <polyline points="7 10 12 15 17 10"/>
          <line x1="12" y1="15" x2="12" y2="3"/>
        </svg>
      </button>
    </div>
  </div>
</template>
