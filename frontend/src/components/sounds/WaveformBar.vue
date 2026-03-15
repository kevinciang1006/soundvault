<script setup lang="ts">
defineProps<{
  isPlaying: boolean
}>()

const delays = ['0ms', '100ms', '200ms', '150ms', '50ms']
</script>

<template>
  <div class="flex items-end gap-0.5 h-5" aria-hidden="true">
    <div
      v-for="(delay, i) in delays"
      :key="i"
      class="w-0.5 rounded-full bg-primary transition-all"
      :class="isPlaying ? 'animate-waveform' : ''"
      :style="`
        height: ${isPlaying ? '100%' : '40%'};
        animation-delay: ${delay};
        animation-duration: 0.8s;
      `"
    />
  </div>
</template>

<style scoped>
@keyframes waveform {
  0%, 100% { height: 30%; }
  50% { height: 100%; }
}

.animate-waveform {
  animation: waveform 0.8s ease-in-out infinite;
}
</style>
