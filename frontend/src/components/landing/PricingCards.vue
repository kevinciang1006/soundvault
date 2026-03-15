<script setup lang="ts">
const plans = [
  {
    name: 'Free',
    price: '$0',
    period: '/month',
    description: 'Perfect for exploring',
    cta: 'Get started free',
    ctaStyle: 'border border-border text-text-secondary hover:border-primary hover:text-text-primary',
    highlighted: false,
    features: [
      { text: '100 downloads/month', included: true },
      { text: 'Standard quality (MP3)', included: true },
      { text: 'Personal use only', included: true },
      { text: 'Commercial license', included: false },
      { text: 'Stems & MIDI', included: false },
      { text: 'Priority support', included: false },
    ],
  },
  {
    name: 'Creator',
    price: '$7.99',
    period: '/month',
    description: 'Best for working producers',
    cta: 'Start Creator plan',
    ctaStyle: 'bg-primary text-white hover:bg-primary/90 shadow-glow',
    highlighted: true,
    badge: 'Most Popular',
    features: [
      { text: 'Unlimited downloads', included: true },
      { text: 'Lossless quality (WAV)', included: true },
      { text: 'Commercial license', included: true },
      { text: 'Stems & MIDI files', included: true },
      { text: 'Early access to drops', included: true },
      { text: 'Priority support', included: false },
    ],
  },
  {
    name: 'Pro',
    price: '$14.99',
    period: '/month',
    description: 'For studios & power users',
    cta: 'Go Pro',
    ctaStyle: 'border border-border text-text-secondary hover:border-primary hover:text-text-primary',
    highlighted: false,
    features: [
      { text: 'Everything in Creator', included: true },
      { text: 'Team collaboration (5 seats)', included: true },
      { text: 'API access', included: true },
      { text: 'White-label licensing', included: true },
      { text: 'Custom pack requests', included: true },
      { text: 'Priority support', included: true },
    ],
  },
]
</script>

<template>
  <section class="py-24 bg-surface">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16">
        <h2 class="font-serif text-4xl md:text-5xl text-text-primary mb-4">
          Simple pricing
        </h2>
        <p class="text-lg font-sans text-text-secondary">
          Start free. Upgrade when you're ready.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 items-stretch">
        <div
          v-for="plan in plans"
          :key="plan.name"
          class="relative bg-background rounded-xl p-8 flex flex-col transition-all duration-300"
          :class="plan.highlighted
            ? 'border-2 border-primary shadow-glow scale-[1.02]'
            : 'border border-border hover:border-primary/30'"
        >
          <!-- Badge -->
          <div
            v-if="plan.badge"
            class="absolute -top-3 left-1/2 -translate-x-1/2 bg-primary text-white text-xs font-sans font-semibold px-3 py-1 rounded-full"
          >
            {{ plan.badge }}
          </div>

          <div class="mb-6">
            <h3 class="font-sans text-lg font-semibold text-text-primary mb-1">{{ plan.name }}</h3>
            <p class="text-sm font-sans text-text-muted mb-4">{{ plan.description }}</p>
            <div class="flex items-baseline gap-1">
              <span class="font-serif text-4xl text-text-primary">{{ plan.price }}</span>
              <span class="text-sm font-sans text-text-muted">{{ plan.period }}</span>
            </div>
          </div>

          <ul class="space-y-3 mb-8 flex-1">
            <li
              v-for="feature in plan.features"
              :key="feature.text"
              class="flex items-center gap-3 text-sm font-sans"
              :class="feature.included ? 'text-text-secondary' : 'text-text-muted'"
            >
              <span
                class="flex-shrink-0 w-4 h-4 rounded-full flex items-center justify-center text-xs"
                :class="feature.included ? 'bg-success/20 text-success' : 'bg-surface-raised text-text-muted'"
              >
                {{ feature.included ? '✓' : '✕' }}
              </span>
              {{ feature.text }}
            </li>
          </ul>

          <button
            class="w-full py-3 rounded-xl font-sans font-semibold text-sm transition-all duration-200"
            :class="plan.ctaStyle"
          >
            {{ plan.cta }}
          </button>
        </div>
      </div>

      <div class="text-center mt-8">
        <a href="#" class="text-sm font-sans text-text-muted hover:text-primary transition-colors duration-200">
          See full comparison &rarr;
        </a>
      </div>
    </div>
  </section>
</template>
