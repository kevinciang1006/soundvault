<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'

const headlineVisible = ref(false)
const subtitleVisible = ref(false)
const buttonsVisible = ref(false)
const proofVisible = ref(false)

onMounted(() => {
  setTimeout(() => { headlineVisible.value = true }, 50)
  setTimeout(() => { subtitleVisible.value = true }, 150)
  setTimeout(() => { buttonsVisible.value = true }, 250)
  setTimeout(() => { proofVisible.value = true }, 400)
})
</script>

<template>
  <section class="relative min-h-screen flex items-center justify-center overflow-hidden bg-background">
    <!-- Radial gradient background glow -->
    <div
      class="absolute inset-0 pointer-events-none"
      style="background: radial-gradient(ellipse 80% 60% at 50% 40%, rgba(99,102,241,0.12) 0%, rgba(6,182,212,0.06) 40%, transparent 70%);"
    />
    <!-- Additional subtle noise texture -->
    <div class="absolute inset-0 pointer-events-none opacity-[0.03]" style="background-image: url('data:image/svg+xml,%3Csvg width=\'200\' height=\'200\' viewBox=\'0 0 200 200\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cfilter id=\'noise\'%3E%3CfeTurbulence type=\'fractalNoise\' baseFrequency=\'0.9\' numOctaves=\'4\' stitchTiles=\'stitch\'/%3E%3C/filter%3E%3Crect width=\'100%25\' height=\'100%25\' filter=\'url(%23noise)\'/%3E%3C/svg%3E');" />

    <div class="relative z-10 text-center max-w-4xl mx-auto px-6">
      <!-- Headline -->
      <h1
        class="font-serif text-5xl sm:text-6xl md:text-7xl lg:text-8xl text-text-primary leading-tight transition-all duration-600"
        :class="headlineVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-5'"
        style="transition: opacity 600ms ease, transform 600ms ease;"
      >
        Every sound you<br />
        <span class="bg-gradient-to-r from-primary via-accent to-primary bg-clip-text text-transparent">
          need.
        </span>
      </h1>

      <!-- Subtitle -->
      <p
        class="mt-6 text-lg sm:text-xl md:text-2xl font-sans text-text-secondary max-w-2xl mx-auto leading-relaxed transition-all"
        :class="subtitleVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-5'"
        style="transition: opacity 600ms ease 100ms, transform 600ms ease 100ms;"
      >
        500,000+ royalty-free samples from the world's best producers.
      </p>

      <!-- Buttons -->
      <div
        class="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4 transition-all"
        :class="buttonsVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-5'"
        style="transition: opacity 600ms ease 200ms, transform 600ms ease 200ms;"
      >
        <button class="px-8 py-4 bg-primary hover:bg-primary/90 text-white font-sans font-semibold text-base rounded-xl shadow-glow transition-all duration-200 hover:shadow-[0_0_40px_rgba(99,102,241,0.4)] hover:scale-105">
          Start for free
        </button>
        <RouterLink
          to="/sounds"
          class="px-8 py-4 border border-border hover:border-primary text-text-secondary hover:text-text-primary font-sans font-medium text-base rounded-xl transition-all duration-200 hover:bg-surface-raised"
        >
          Browse sounds &rarr;
        </RouterLink>
      </div>

      <!-- Social proof -->
      <div
        class="mt-8 flex items-center justify-center gap-3 transition-all"
        :class="proofVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-5'"
        style="transition: opacity 600ms ease 400ms, transform 600ms ease 400ms;"
      >
        <div class="flex -space-x-2">
          <div v-for="i in 4" :key="i" class="w-7 h-7 rounded-full border-2 border-background" :style="`background: hsl(${i * 60 + 200}, 60%, 50%)`" />
        </div>
        <span class="text-sm font-sans text-text-muted">
          Trusted by <span class="text-text-secondary font-medium">2M+ producers</span> worldwide
        </span>
      </div>
    </div>

    <!-- Bottom fade -->
    <div class="absolute bottom-0 left-0 right-0 h-32 pointer-events-none" style="background: linear-gradient(transparent, #0a0a0f);" />
  </section>
</template>
