<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from '@/components/layout/Navbar.vue'
import FilterBar from '@/components/sounds/FilterBar.vue'
import PackCard from '@/components/sounds/PackCard.vue'
import SampleRow from '@/components/sounds/SampleRow.vue'
import AudioPlayer from '@/components/sounds/AudioPlayer.vue'
import { useSamples } from '@/composables/useSamples'
import { usePlayerStore } from '@/stores/playerStore'
import type { Pack, Sample } from '@/types'

const route = useRoute()
const playerStore = usePlayerStore()
const { samples, packs, total, isLoading, filters, fetchSamples, fetchPacks, resetFilters } = useSamples()

const filterBarOpen = ref(false)
const currentOffset = ref(0)

onMounted(async () => {
  // Apply query param for key from analyze page
  if (route.query.key) {
    filters.key = route.query.key as string
  }
  await fetchPacks()
  await fetchSamples(0)
})

watch(
  () => route.query.key,
  (key) => {
    if (key) filters.key = key as string
  }
)

function onFiltersUpdated(newFilters: typeof filters) {
  Object.assign(filters, newFilters)
}

function onPackSelected(pack: Pack) {
  if (filters.pack_id === pack.id) {
    filters.pack_id = null
  } else {
    filters.pack_id = pack.id
  }
}

function handleReset() {
  resetFilters()
}

async function loadMore() {
  currentOffset.value += 20
  await fetchSamples(currentOffset.value)
}

watch(filters, () => {
  currentOffset.value = 0
}, { deep: true })

function playSample(sample: Sample) {
  playerStore.play(sample)
}

const sortOptions = [
  { value: 'trending', label: 'Trending' },
  { value: 'newest', label: 'Newest' },
  { value: 'bpm_asc', label: 'BPM (Low → High)' },
  { value: 'bpm_desc', label: 'BPM (High → Low)' },
]
</script>

<template>
  <div class="min-h-screen bg-background flex flex-col">
    <Navbar />

    <div class="flex flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8 gap-6">
      <!-- Filter bar -->
      <FilterBar
        :filters="filters"
        :is-open="filterBarOpen"
        @update:filters="onFiltersUpdated"
        @close="filterBarOpen = false"
        @reset="handleReset"
      />

      <!-- Main content -->
      <main class="flex-1 min-w-0">
        <!-- Top bar -->
        <div class="flex items-center justify-between mb-6 gap-4">
          <!-- Mobile filter toggle -->
          <button
            class="md:hidden flex items-center gap-2 text-sm font-sans text-text-secondary border border-border rounded-lg px-3 py-2 hover:border-primary transition-colors"
            @click="filterBarOpen = true"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="4" y1="6" x2="20" y2="6"/><line x1="8" y1="12" x2="16" y2="12"/><line x1="10" y1="18" x2="14" y2="18"/>
            </svg>
            Filters
          </button>

          <p class="text-sm font-sans text-text-muted">
            <span class="text-text-secondary font-medium">{{ total }}</span> samples found
          </p>

          <select
            v-model="filters.sort"
            class="bg-surface border border-border rounded-lg px-3 py-2 text-sm font-sans text-text-secondary focus:outline-none focus:border-primary transition-colors cursor-pointer"
          >
            <option v-for="opt in sortOptions" :key="opt.value" :value="opt.value">
              {{ opt.label }}
            </option>
          </select>
        </div>

        <!-- Pack scroll row -->
        <div class="mb-6">
          <h3 class="text-xs font-sans font-semibold text-text-muted uppercase tracking-widest mb-3">Packs</h3>
          <div class="flex gap-3 overflow-x-auto pb-3 scrollbar-hide">
            <PackCard
              v-for="pack in packs"
              :key="pack.id"
              :pack="pack"
              :is-selected="filters.pack_id === pack.id"
              @pack-selected="onPackSelected"
            />
          </div>
        </div>

        <!-- Sample list -->
        <div class="bg-surface border border-border rounded-xl overflow-hidden">
          <!-- Loading skeleton -->
          <div v-if="isLoading && samples.length === 0">
            <div
              v-for="i in 8"
              :key="i"
              class="flex items-center gap-4 px-4 py-3 border-b border-border/50 last:border-none"
            >
              <div class="w-8 h-8 rounded-full bg-surface-raised animate-pulse" />
              <div class="flex-1 space-y-1.5">
                <div class="h-3 bg-surface-raised rounded animate-pulse w-3/4" />
                <div class="h-2 bg-surface-raised rounded animate-pulse w-1/2" />
              </div>
              <div class="flex gap-2">
                <div class="h-5 w-16 bg-surface-raised rounded animate-pulse" />
                <div class="h-5 w-10 bg-surface-raised rounded animate-pulse" />
              </div>
            </div>
          </div>

          <!-- No results -->
          <div v-else-if="!isLoading && samples.length === 0" class="py-20 text-center">
            <div class="text-text-muted mb-3">
              <svg class="mx-auto" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
              </svg>
            </div>
            <p class="font-sans text-text-secondary font-medium mb-1">No samples found</p>
            <p class="text-sm font-sans text-text-muted">Try adjusting your filters</p>
            <button class="mt-4 text-sm font-sans text-primary hover:underline" @click="handleReset">
              Clear filters
            </button>
          </div>

          <!-- Sample rows -->
          <div v-else>
            <SampleRow
              v-for="sample in samples"
              :key="sample.id"
              :sample="sample"
              :is-current-sample="playerStore.currentSample?.id === sample.id"
              :is-playing="playerStore.isPlaying && playerStore.currentSample?.id === sample.id"
              class="border-b border-border/50 last:border-none"
              @play="playSample"
            />
          </div>
        </div>

        <!-- Load more -->
        <div v-if="samples.length < total && !isLoading" class="flex justify-center mt-6">
          <button
            class="px-6 py-2.5 border border-border rounded-xl text-sm font-sans text-text-secondary hover:border-primary hover:text-text-primary transition-all duration-200"
            @click="loadMore"
          >
            Load more samples
          </button>
        </div>

        <!-- Loading more indicator -->
        <div v-if="isLoading && samples.length > 0" class="flex justify-center mt-6">
          <div class="flex gap-1.5">
            <div v-for="i in 3" :key="i" class="w-2 h-2 rounded-full bg-primary animate-bounce" :style="`animation-delay: ${(i-1) * 150}ms`" />
          </div>
        </div>
      </main>
    </div>

    <!-- Spacer for audio player -->
    <div v-if="playerStore.currentSample" class="h-20" />

    <AudioPlayer />
  </div>
</template>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
