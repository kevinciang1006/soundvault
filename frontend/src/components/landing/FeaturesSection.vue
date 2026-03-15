<script setup lang="ts">
const features = [
  {
    number: '500K+',
    title: 'Sounds',
    description: 'From trap 808s to ambient pads, every genre covered. Discover the perfect sound for any project.',
    gradient: 'from-primary to-accent',
  },
  {
    number: '100%',
    title: 'Royalty-Free',
    description: 'Use in commercial projects with zero clearance headaches. License once, use forever.',
    gradient: 'from-accent to-success',
  },
  {
    number: 'New',
    title: 'Drops Weekly',
    description: 'Fresh packs from top producers added every week. Stay ahead of the curve with the latest sounds.',
    gradient: 'from-success to-primary',
  },
]
</script>

<template>
  <section class="py-24 bg-background">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16">
        <h2 class="font-serif text-4xl md:text-5xl text-text-primary mb-4">
          Built for creators
        </h2>
        <p class="text-lg font-sans text-text-secondary max-w-xl mx-auto">
          Everything you need to find the perfect sound and keep making music.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div
          v-for="feature in features"
          :key="feature.title"
          class="bg-surface border border-border rounded-xl p-8 hover:border-primary/30 transition-all duration-300 hover:shadow-lg group"
        >
          <div
            class="inline-block font-serif text-5xl md:text-6xl font-bold bg-gradient-to-br bg-clip-text text-transparent mb-4"
            :class="`bg-gradient-to-br ${feature.gradient}`"
          >
            {{ feature.number }}
          </div>
          <h3 class="font-sans text-xl font-semibold text-text-primary mb-3">
            {{ feature.title }}
          </h3>
          <p class="font-sans text-text-secondary leading-relaxed">
            {{ feature.description }}
          </p>
        </div>
      </div>
    </div>
  </section>
</template>
