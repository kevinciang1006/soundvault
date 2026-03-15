<script setup lang="ts">
import { computed } from 'vue'
import type { SampleFilters } from '@/types'

const props = defineProps<{
  filters: SampleFilters
  isOpen: boolean
}>()

const emit = defineEmits<{
  (e: 'update:filters', filters: SampleFilters): void
  (e: 'close'): void
  (e: 'reset'): void
}>()

const genres = ['Hip Hop', 'Trap', 'House', 'Techno', 'R&B', 'Pop', 'Drum & Bass', 'Ambient']

const keys = [
  'All Keys', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B',
  'Cm', 'C#m', 'Dm', 'D#m', 'Em', 'Fm', 'F#m', 'Gm', 'G#m', 'Am', 'A#m', 'Bm',
]

const sampleTypes = [
  { value: 'loop', label: 'Loops' },
  { value: 'one_shot', label: 'One-Shots' },
  { value: 'vocal', label: 'Vocals' },
  { value: 'fx', label: 'FX' },
]

function updateFilter<K extends keyof SampleFilters>(key: K, value: SampleFilters[K]) {
  emit('update:filters', { ...props.filters, [key]: value })
}

function toggleGenre(genre: string) {
  const current = props.filters.genre
  updateFilter('genre', current === genre ? '' : genre)
}

function toggleSampleType(type: string) {
  const current = props.filters.sample_type
  updateFilter('sample_type', current === type ? '' : type)
}

const bpmRangePercent = computed(() => {
  const min = ((props.filters.bpm_min - 60) / (200 - 60)) * 100
  const max = ((props.filters.bpm_max - 60) / (200 - 60)) * 100
  return { min, max }
})
</script>

<template>
  <!-- Mobile overlay -->
  <Teleport to="body">
    <div
      v-if="isOpen"
      class="fixed inset-0 bg-background/80 backdrop-blur-sm z-40 md:hidden"
      @click="emit('close')"
    />
  </Teleport>

  <!-- Sidebar -->
  <aside
    class="fixed md:sticky top-0 md:top-20 left-0 h-full md:h-auto w-72 bg-surface border-r md:border border-border md:rounded-xl p-6 z-50 md:z-auto overflow-y-auto transition-transform duration-300"
    :class="isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'"
    style="max-height: calc(100vh - 6rem);"
  >
    <div class="flex items-center justify-between mb-6 md:hidden">
      <h3 class="font-sans font-semibold text-text-primary">Filters</h3>
      <button class="text-text-muted hover:text-text-primary" @click="emit('close')">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M18 6L6 18M6 6l12 12"/>
        </svg>
      </button>
    </div>

    <!-- Search -->
    <div class="mb-6">
      <label class="text-xs font-sans font-semibold text-text-muted uppercase tracking-widest mb-2 block">Search</label>
      <div class="relative">
        <svg class="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
        </svg>
        <input
          :value="filters.q"
          type="text"
          placeholder="Search samples..."
          class="w-full bg-background border border-border rounded-lg pl-9 pr-4 py-2.5 text-sm font-sans text-text-primary placeholder-text-muted focus:outline-none focus:border-primary transition-colors"
          @input="updateFilter('q', ($event.target as HTMLInputElement).value)"
        />
      </div>
    </div>

    <!-- Genre -->
    <div class="mb-6">
      <label class="text-xs font-sans font-semibold text-text-muted uppercase tracking-widest mb-3 block">Genre</label>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="genre in genres"
          :key="genre"
          class="px-2.5 py-1 text-xs font-sans rounded-lg border transition-all duration-200"
          :class="filters.genre === genre
            ? 'bg-primary/20 border-primary text-primary'
            : 'bg-background border-border text-text-muted hover:border-primary/40 hover:text-text-secondary'"
          @click="toggleGenre(genre)"
        >
          {{ genre }}
        </button>
      </div>
    </div>

    <!-- BPM Range -->
    <div class="mb-6">
      <label class="text-xs font-sans font-semibold text-text-muted uppercase tracking-widest mb-3 block">BPM Range</label>
      <div class="flex items-center gap-2 mb-3">
        <input
          :value="filters.bpm_min"
          type="number"
          min="60"
          max="200"
          class="w-20 bg-background border border-border rounded-lg px-2 py-1.5 text-sm font-mono text-text-primary focus:outline-none focus:border-primary text-center"
          @input="updateFilter('bpm_min', Number(($event.target as HTMLInputElement).value))"
        />
        <span class="text-text-muted text-xs">—</span>
        <input
          :value="filters.bpm_max"
          type="number"
          min="60"
          max="200"
          class="w-20 bg-background border border-border rounded-lg px-2 py-1.5 text-sm font-mono text-text-primary focus:outline-none focus:border-primary text-center"
          @input="updateFilter('bpm_max', Number(($event.target as HTMLInputElement).value))"
        />
      </div>
      <!-- Visual bar -->
      <div class="h-1.5 bg-surface-raised rounded-full relative overflow-hidden">
        <div
          class="absolute top-0 bottom-0 bg-primary rounded-full"
          :style="`left: ${bpmRangePercent.min}%; right: ${100 - bpmRangePercent.max}%`"
        />
      </div>
    </div>

    <!-- Key -->
    <div class="mb-6">
      <label class="text-xs font-sans font-semibold text-text-muted uppercase tracking-widest mb-2 block">Key</label>
      <select
        :value="filters.key"
        class="w-full bg-background border border-border rounded-lg px-3 py-2.5 text-sm font-sans text-text-primary focus:outline-none focus:border-primary transition-colors appearance-none cursor-pointer"
        @change="updateFilter('key', ($event.target as HTMLSelectElement).value === 'All Keys' ? '' : ($event.target as HTMLSelectElement).value)"
      >
        <option v-for="key in keys" :key="key" :value="key === 'All Keys' ? '' : key">
          {{ key }}
        </option>
      </select>
    </div>

    <!-- Sample Type -->
    <div class="mb-8">
      <label class="text-xs font-sans font-semibold text-text-muted uppercase tracking-widest mb-3 block">Sample Type</label>
      <div class="space-y-2">
        <button
          v-for="type in sampleTypes"
          :key="type.value"
          class="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-sans border transition-all duration-200"
          :class="filters.sample_type === type.value
            ? 'bg-primary/20 border-primary text-primary'
            : 'bg-background border-border text-text-muted hover:border-primary/40 hover:text-text-secondary'"
          @click="toggleSampleType(type.value)"
        >
          <span
            class="w-4 h-4 rounded border flex-shrink-0 flex items-center justify-center text-xs"
            :class="filters.sample_type === type.value ? 'border-primary bg-primary text-white' : 'border-border'"
          >
            <span v-if="filters.sample_type === type.value">✓</span>
          </span>
          {{ type.label }}
        </button>
      </div>
    </div>

    <!-- Clear filters -->
    <button
      class="text-sm font-sans text-text-muted hover:text-primary transition-colors duration-200 underline underline-offset-4"
      @click="emit('reset')"
    >
      Clear all filters
    </button>
  </aside>
</template>
