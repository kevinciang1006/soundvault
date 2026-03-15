<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  (e: 'file-selected', file: File): void
}>()

const isDragOver = ref(false)
const error = ref('')
const fileInputRef = ref<HTMLInputElement | null>(null)

const ALLOWED_EXTENSIONS = ['.mp3', '.wav', '.flac', '.ogg', '.m4a']
const MAX_SIZE = 20 * 1024 * 1024 // 20MB

function validateFile(file: File): string | null {
  const ext = '.' + file.name.split('.').pop()?.toLowerCase()
  if (!ALLOWED_EXTENSIONS.includes(ext)) {
    return `Unsupported file type. Allowed: ${ALLOWED_EXTENSIONS.join(', ')}`
  }
  if (file.size > MAX_SIZE) {
    return 'File too large. Maximum size is 20MB.'
  }
  return null
}

function handleFile(file: File) {
  error.value = ''
  const err = validateFile(file)
  if (err) {
    error.value = err
    return
  }
  emit('file-selected', file)
}

function onDrop(event: DragEvent) {
  isDragOver.value = false
  const file = event.dataTransfer?.files?.[0]
  if (file) handleFile(file)
}

function onFileInput(event: Event) {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (file) handleFile(file)
}

function onClick() {
  fileInputRef.value?.click()
}
</script>

<template>
  <div
    class="relative border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all duration-200 group"
    :class="isDragOver
      ? 'border-primary bg-primary/5'
      : 'border-border hover:border-primary/50 hover:bg-surface-raised/50'"
    @dragenter.prevent="isDragOver = true"
    @dragover.prevent="isDragOver = true"
    @dragleave.prevent="isDragOver = false"
    @drop.prevent="onDrop"
    @click="onClick"
  >
    <input
      ref="fileInputRef"
      type="file"
      accept=".mp3,.wav,.flac,.ogg,.m4a"
      class="hidden"
      @change="onFileInput"
    />

    <!-- Upload icon -->
    <div
      class="mx-auto w-16 h-16 rounded-full flex items-center justify-center mb-6 transition-all duration-200"
      :class="isDragOver ? 'bg-primary/20 scale-110' : 'bg-surface-raised group-hover:bg-primary/10'"
    >
      <svg
        width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"
        :class="isDragOver ? 'text-primary' : 'text-text-muted group-hover:text-primary'"
        class="transition-colors duration-200"
      >
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
        <polyline points="17 8 12 3 7 8"/>
        <line x1="12" y1="3" x2="12" y2="15"/>
      </svg>
    </div>

    <p class="font-sans text-lg font-medium text-text-primary mb-2">
      <span v-if="isDragOver">Release to analyze</span>
      <span v-else>Drop your audio file here or <span class="text-primary underline underline-offset-2">click to browse</span></span>
    </p>
    <p class="text-sm font-sans text-text-muted">
      Supports MP3, WAV, FLAC, OGG, M4A &mdash; up to 20MB
    </p>

    <!-- Error -->
    <div v-if="error" class="mt-4 px-4 py-2 bg-red-500/10 border border-red-500/30 rounded-lg" @click.stop>
      <p class="text-sm font-sans text-red-400">{{ error }}</p>
    </div>
  </div>
</template>
