<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

const route = useRoute()
const mobileOpen = ref(false)

const navLinks = [
  { name: 'Sounds', path: '/sounds' },
  { name: 'Plans', path: '/plans' },
  { name: 'Analyze', path: '/analyze' },
]
</script>

<template>
  <header class="sticky top-0 z-50 backdrop-blur-md bg-background/80 border-b border-border">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <RouterLink to="/" class="flex items-center gap-2 group">
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none" class="text-primary">
            <path d="M4 20 Q7 8 10 14 Q13 20 14 10 Q15 0 18 14 Q21 20 24 8" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
          </svg>
          <span class="font-serif text-xl text-text-primary group-hover:text-primary transition-colors duration-200">
            SoundVault
          </span>
        </RouterLink>

        <!-- Center Nav -->
        <nav class="hidden md:flex items-center gap-8">
          <RouterLink
            v-for="link in navLinks"
            :key="link.path"
            :to="link.path"
            class="relative text-sm font-sans font-medium text-text-secondary hover:text-text-primary transition-colors duration-200 pb-1"
            :class="{ 'text-text-primary': route.path === link.path }"
          >
            {{ link.name }}
            <span
              v-if="route.path === link.path"
              class="absolute bottom-0 left-0 right-0 h-0.5 bg-primary rounded-full"
            />
          </RouterLink>
        </nav>

        <!-- Right CTAs -->
        <div class="hidden md:flex items-center gap-3">
          <button class="text-sm font-sans font-medium text-text-secondary hover:text-text-primary transition-colors duration-200 px-4 py-2 rounded-lg border border-transparent hover:border-border">
            Log in
          </button>
          <button class="text-sm font-sans font-semibold text-white bg-primary hover:bg-primary/90 transition-colors duration-200 px-4 py-2 rounded-lg shadow-glow">
            Try Free
          </button>
        </div>

        <!-- Mobile hamburger -->
        <button
          class="md:hidden text-text-secondary hover:text-text-primary transition-colors p-2"
          @click="mobileOpen = !mobileOpen"
          aria-label="Toggle menu"
        >
          <svg v-if="!mobileOpen" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 12h18M3 6h18M3 18h18"/>
          </svg>
          <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 6L6 18M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Mobile Menu -->
      <div v-if="mobileOpen" class="md:hidden pb-4 border-t border-border mt-2 pt-4">
        <nav class="flex flex-col gap-3">
          <RouterLink
            v-for="link in navLinks"
            :key="link.path"
            :to="link.path"
            class="text-sm font-sans font-medium text-text-secondary hover:text-text-primary transition-colors duration-200 py-2"
            :class="{ 'text-primary': route.path === link.path }"
            @click="mobileOpen = false"
          >
            {{ link.name }}
          </RouterLink>
        </nav>
        <div class="flex gap-3 mt-4">
          <button class="flex-1 text-sm font-sans font-medium text-text-secondary border border-border rounded-lg py-2 hover:border-primary transition-colors">
            Log in
          </button>
          <button class="flex-1 text-sm font-sans font-semibold text-white bg-primary rounded-lg py-2">
            Try Free
          </button>
        </div>
      </div>
    </div>
  </header>
</template>
