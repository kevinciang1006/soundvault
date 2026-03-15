<script setup lang="ts">
import { usePlayerStore } from '@/stores/playerStore'
import type { Sample } from '@/types'

const playerStore = usePlayerStore()

const mockSamples: Sample[] = [
  { id: 1, pack_id: 1, pack_name: 'Tokyo Trap Vol. 1', pack_creator: 'KxngProd', filename: 'TTR_TKYO_140_LPP_drums_Am.wav', genre: 'Trap', sample_type: 'loop', bpm: 140, key: 'Am', duration_seconds: 4, is_premium: false, play_count: 3200 },
  { id: 2, pack_id: 2, pack_name: 'Deep House Essentials', pack_creator: 'WaveForge', filename: 'DHE_DHSE_124_LPP_chord_Fm.wav', genre: 'House', sample_type: 'loop', bpm: 124, key: 'Fm', duration_seconds: 8, is_premium: false, play_count: 2100 },
  { id: 3, pack_id: 3, pack_name: 'Lo-Fi Dreams', pack_creator: 'CloudBeats', filename: 'LFD_LOFI_85_LPP_melody_C.wav', genre: 'R&B', sample_type: 'loop', bpm: 85, key: 'C', duration_seconds: 6, is_premium: false, play_count: 4500 },
  { id: 4, pack_id: 5, pack_name: 'Boom Bap Classics', pack_creator: 'OldSoul', filename: 'BBC_BOOM_92_OSS_kick_D.wav', genre: 'Hip Hop', sample_type: 'one_shot', bpm: 92, key: 'D', duration_seconds: 0.5, is_premium: false, play_count: 1800 },
  { id: 5, pack_id: 6, pack_name: 'Future Bass Elements', pack_creator: 'NeonSynth', filename: 'FBE_FBAS_128_LPP_arp_F#m.wav', genre: 'Pop', sample_type: 'loop', bpm: 128, key: 'F#m', duration_seconds: 4, is_premium: true, play_count: 2700 },
  { id: 6, pack_id: 7, pack_name: 'Ambient Textures', pack_creator: 'SilentDrift', filename: 'AMB_AMBT_70_LPP_groove_G.wav', genre: 'Ambient', sample_type: 'loop', bpm: 70, key: 'G', duration_seconds: 16, is_premium: false, play_count: 980 },
  { id: 7, pack_id: 8, pack_name: 'Drum & Bass Fury', pack_creator: 'BreakCore', filename: 'DBF_DNBF_174_LPP_bounce_Em.wav', genre: 'Drum & Bass', sample_type: 'loop', bpm: 174, key: 'Em', duration_seconds: 4, is_premium: true, play_count: 3100 },
  { id: 8, pack_id: 9, pack_name: 'Vocal Chops Vol. 2', pack_creator: 'VoxLab', filename: 'VCV_VCLP_138_VCL_chop_A#m.wav', genre: 'Trap', sample_type: 'vocal', bpm: 138, key: 'A#m', duration_seconds: 2, is_premium: false, play_count: 1500 },
]
</script>

<template>
  <section class="py-16 bg-background overflow-hidden">
    <div class="max-w-7xl mx-auto px-4 mb-8">
      <p class="text-xs font-sans font-semibold text-text-muted uppercase tracking-widest text-center">
        Preview samples from our library
      </p>
    </div>

    <div class="relative">
      <!-- Fade masks -->
      <div class="absolute left-0 top-0 bottom-0 w-24 z-10 pointer-events-none" style="background: linear-gradient(to right, #0a0a0f, transparent);" />
      <div class="absolute right-0 top-0 bottom-0 w-24 z-10 pointer-events-none" style="background: linear-gradient(to left, #0a0a0f, transparent);" />

      <div class="strip-container overflow-hidden">
        <div class="strip-inner flex gap-4 w-max">
          <!-- Render twice for seamless loop -->
          <template v-for="pass in 2" :key="pass">
            <div
              v-for="sample in mockSamples"
              :key="`${pass}-${sample.id}`"
              class="flex-shrink-0 w-56 bg-surface border border-border rounded-xl p-4 cursor-pointer group hover:border-primary/40 transition-all duration-200"
              style="perspective: 800px;"
              @mouseenter="($event.currentTarget as HTMLElement).style.transform = 'rotateY(5deg) translateY(-2px)'"
              @mouseleave="($event.currentTarget as HTMLElement).style.transform = 'rotateY(0deg) translateY(0)'"
            >
              <p class="font-mono text-xs text-text-primary truncate mb-3" :title="sample.filename">
                {{ sample.filename }}
              </p>
              <div class="flex items-center gap-2 mb-4">
                <span class="px-1.5 py-0.5 bg-accent/20 text-accent font-mono text-xs rounded">
                  {{ sample.bpm }} BPM
                </span>
                <span class="px-1.5 py-0.5 bg-primary/20 text-primary font-mono text-xs rounded">
                  {{ sample.key }}
                </span>
              </div>
              <button
                class="w-full flex items-center justify-center gap-2 py-2 rounded-lg bg-surface-raised hover:bg-primary/20 hover:text-primary text-text-secondary transition-all duration-200 text-sm font-sans"
                @click.stop="playerStore.play(sample)"
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M8 5v14l11-7z"/>
                </svg>
                Play
              </button>
            </div>
          </template>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.strip-container {
  width: 100%;
}

.strip-inner {
  animation: scroll-left 40s linear infinite;
  transition: transform 0.3s ease;
}

.strip-container:hover .strip-inner {
  animation-play-state: paused;
}

@keyframes scroll-left {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-50%);
  }
}
</style>
