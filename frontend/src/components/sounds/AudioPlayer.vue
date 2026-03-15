<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { usePlayerStore } from '@/stores/playerStore'

const playerStore = usePlayerStore()

const progressWidth = ref(0)
let progressInterval: ReturnType<typeof setInterval> | null = null
let progressStart = 0

function startProgress(duration: number) {
  if (progressInterval) clearInterval(progressInterval)
  progressWidth.value = 0
  progressStart = Date.now()
  const totalMs = Math.min(duration, 3) * 1000

  progressInterval = setInterval(() => {
    const elapsed = Date.now() - progressStart
    progressWidth.value = Math.min((elapsed / totalMs) * 100, 100)
    if (progressWidth.value >= 100) {
      clearInterval(progressInterval!)
      progressInterval = null
    }
  }, 50)
}

watch(() => playerStore.currentSample, (sample) => {
  if (sample && playerStore.isPlaying) {
    startProgress(sample.duration_seconds)
  }
})

watch(() => playerStore.isPlaying, (playing) => {
  if (!playing) {
    if (progressInterval) clearInterval(progressInterval)
  } else if (playerStore.currentSample) {
    startProgress(playerStore.currentSample.duration_seconds)
  }
})

const formattedDuration = computed(() => {
  if (!playerStore.currentSample) return '0:00'
  const total = Math.round(playerStore.currentSample.duration_seconds)
  const m = Math.floor(total / 60)
  const s = total % 60
  return `${m}:${s.toString().padStart(2, '0')}`
})
</script>

<template>
  <Transition name="slide-up">
    <div
      v-if="playerStore.currentSample"
      class="fixed bottom-0 left-0 right-0 z-50 bg-surface/95 backdrop-blur-lg border-t border-border"
    >
      <!-- Progress bar -->
      <div class="h-0.5 bg-surface-raised">
        <div
          class="h-full bg-gradient-to-r from-primary to-accent transition-none"
          :style="`width: ${progressWidth}%`"
        />
      </div>

      <div class="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center gap-4">
        <!-- Sample info -->
        <div class="flex-1 min-w-0 hidden sm:block">
          <p class="font-mono text-sm text-text-primary truncate">
            {{ playerStore.currentSample?.filename }}
          </p>
          <p class="text-xs font-sans text-text-muted truncate">
            {{ playerStore.currentSample?.pack_name }}
          </p>
        </div>

        <!-- Controls -->
        <div class="flex items-center gap-3 mx-auto sm:mx-0">
          <button
            class="text-text-muted hover:text-text-primary transition-colors p-1.5"
            @click="playerStore.prev()"
            title="Previous"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <path d="M19 20L9 12l10-8v16z"/><rect x="5" y="4" width="2" height="16"/>
            </svg>
          </button>

          <button
            class="w-10 h-10 rounded-full bg-primary hover:bg-primary/90 flex items-center justify-center text-white transition-colors shadow-glow"
            @click="playerStore.isPlaying ? playerStore.pause() : playerStore.resume()"
          >
            <svg v-if="playerStore.isPlaying" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
            </svg>
            <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M8 5v14l11-7z"/>
            </svg>
          </button>

          <button
            class="text-text-muted hover:text-text-primary transition-colors p-1.5"
            @click="playerStore.next()"
            title="Next"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <path d="M5 4l10 8-10 8V4z"/><rect x="17" y="4" width="2" height="16"/>
            </svg>
          </button>
        </div>

        <!-- Volume -->
        <div class="flex items-center gap-2 flex-shrink-0">
          <svg class="text-text-muted" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M11 5L6 9H2v6h4l5 4V5zm7.54 2.88a10 10 0 0 1 0 8.24M15.54 7.88a6 6 0 0 1 0 8.24"/>
          </svg>
          <input
            type="range"
            min="0"
            max="1"
            step="0.01"
            :value="playerStore.volume"
            class="w-20 h-1 rounded-full appearance-none bg-surface-raised cursor-pointer accent-primary"
            @input="playerStore.setVolume(Number(($event.target as HTMLInputElement).value))"
          />
        </div>

        <!-- Duration -->
        <span class="text-xs font-mono text-text-muted hidden sm:block">
          {{ formattedDuration }}
        </span>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.slide-up-enter-active {
  transition: transform 300ms ease;
}
.slide-up-leave-active {
  transition: transform 200ms ease;
}
.slide-up-enter-from {
  transform: translateY(100%);
}
.slide-up-leave-to {
  transform: translateY(100%);
}
</style>
