<script setup lang="ts">
import type { Pack } from '@/types'

const props = defineProps<{
  pack: Pack
  isSelected: boolean
}>()

const emit = defineEmits<{
  (e: 'pack-selected', pack: Pack): void
}>()
</script>

<template>
  <button
    class="flex-shrink-0 w-44 rounded-xl overflow-hidden relative group transition-all duration-200 hover:scale-105 text-left"
    :class="isSelected ? 'ring-2 ring-primary ring-offset-2 ring-offset-background' : ''"
    @click="emit('pack-selected', pack)"
  >
    <!-- Gradient background -->
    <div
      class="h-24 w-full"
      :style="`background: linear-gradient(135deg, ${pack.cover_color}, ${pack.cover_color_2})`"
    />

    <!-- Card content -->
    <div class="bg-surface p-3">
      <h4 class="font-serif text-sm text-text-primary leading-snug mb-0.5 truncate">
        {{ pack.name }}
      </h4>
      <p class="text-xs font-sans text-text-muted truncate">{{ pack.creator }}</p>
      <div class="mt-2">
        <span class="px-1.5 py-0.5 bg-surface-raised text-text-muted font-sans text-xs rounded">
          {{ pack.sample_count }} samples
        </span>
      </div>
    </div>

    <!-- Selected overlay glow -->
    <div
      v-if="isSelected"
      class="absolute inset-0 rounded-xl pointer-events-none"
      style="box-shadow: inset 0 0 0 2px rgba(99,102,241,0.6);"
    />
  </button>
</template>
