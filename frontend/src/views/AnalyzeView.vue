<script setup lang="ts">
import Navbar from '@/components/layout/Navbar.vue'
import Footer from '@/components/layout/Footer.vue'
import DropZone from '@/components/analyze/DropZone.vue'
import ResultCard from '@/components/analyze/ResultCard.vue'
import { useAudioAnalysis } from '@/composables/useAudioAnalysis'

const { result, isLoading, error, analyzeFile } = useAudioAnalysis()

function onFileSelected(file: File) {
  analyzeFile(file)
}

function onReset() {
  result.value = null
}
</script>

<template>
  <div class="min-h-screen bg-background flex flex-col">
    <Navbar />

    <main class="flex-1 flex flex-col items-center py-16 px-4">
      <div class="w-full max-w-lg">
        <!-- Headline -->
        <div class="text-center mb-10">
          <h1 class="font-serif text-4xl md:text-5xl text-text-primary mb-3">
            Analyze your sample
          </h1>
          <p class="font-sans text-text-secondary text-lg">
            Upload any audio file and instantly detect BPM, key, and duration.
          </p>
        </div>

        <!-- State: idle -->
        <div v-if="!isLoading && !result">
          <DropZone @file-selected="onFileSelected" />
          <div v-if="error" class="mt-4 px-4 py-3 bg-red-500/10 border border-red-500/30 rounded-xl">
            <p class="text-sm font-sans text-red-400 text-center">{{ error }}</p>
          </div>
        </div>

        <!-- State: loading -->
        <div v-else-if="isLoading" class="text-center py-16">
          <div class="flex items-end justify-center gap-1.5 h-12 mb-6">
            <div
              v-for="(delay, i) in ['0ms', '100ms', '200ms', '150ms', '50ms', '120ms', '80ms']"
              :key="i"
              class="w-1.5 bg-primary rounded-full animate-waveform-loading"
              :style="`animation-delay: ${delay}; height: ${20 + Math.sin(i) * 15}px;`"
            />
          </div>
          <p class="font-sans text-text-secondary font-medium">Analyzing your sample...</p>
          <p class="text-sm font-sans text-text-muted mt-1">This may take a moment</p>
        </div>

        <!-- State: results -->
        <div v-else-if="result">
          <ResultCard :result="result" @reset="onReset" />
        </div>

        <!-- Feature hints -->
        <div v-if="!isLoading && !result" class="mt-10 grid grid-cols-3 gap-4">
          <div class="text-center p-4 bg-surface border border-border rounded-xl">
            <div class="font-serif text-2xl text-primary mb-1">BPM</div>
            <p class="text-xs font-sans text-text-muted">Tempo detection</p>
          </div>
          <div class="text-center p-4 bg-surface border border-border rounded-xl">
            <div class="font-serif text-2xl text-accent mb-1">Key</div>
            <p class="text-xs font-sans text-text-muted">Key detection</p>
          </div>
          <div class="text-center p-4 bg-surface border border-border rounded-xl">
            <div class="font-serif text-2xl text-success mb-1">∿</div>
            <p class="text-xs font-sans text-text-muted">Duration analysis</p>
          </div>
        </div>
      </div>
    </main>

    <Footer />
  </div>
</template>

<style scoped>
@keyframes waveform-loading {
  0%, 100% { transform: scaleY(0.4); opacity: 0.6; }
  50% { transform: scaleY(1.4); opacity: 1; }
}

.animate-waveform-loading {
  animation: waveform-loading 1s ease-in-out infinite;
}
</style>
