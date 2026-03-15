<script setup lang="ts">
import { ref, computed } from 'vue'
import Navbar from '@/components/layout/Navbar.vue'
import Footer from '@/components/layout/Footer.vue'

const isAnnual = ref(false)

const plans = computed(() => [
  {
    name: 'Free',
    monthlyPrice: 0,
    annualPrice: 0,
    description: 'Perfect for exploring SoundVault',
    cta: 'Get started free',
    ctaStyle: 'border border-border text-text-secondary hover:border-primary hover:text-text-primary',
    highlighted: false,
    features: [
      { text: '100 downloads/month', included: true },
      { text: 'MP3 quality (320kbps)', included: true },
      { text: 'Personal use', included: true },
      { text: 'Browse all samples', included: true },
      { text: 'Commercial license', included: false },
      { text: 'WAV/lossless quality', included: false },
      { text: 'Stems & MIDI files', included: false },
      { text: 'Early access drops', included: false },
      { text: 'Team collaboration', included: false },
      { text: 'API access', included: false },
      { text: 'Priority support', included: false },
    ],
  },
  {
    name: 'Creator',
    monthlyPrice: 7.99,
    annualPrice: 7.99 * 10,
    description: 'Best for working producers',
    cta: 'Start Creator plan',
    ctaStyle: 'bg-primary text-white hover:bg-primary/90 shadow-glow',
    highlighted: true,
    badge: 'Most Popular',
    features: [
      { text: 'Unlimited downloads', included: true },
      { text: 'WAV/lossless quality', included: true },
      { text: 'Commercial license', included: true },
      { text: 'Browse all samples', included: true },
      { text: 'Stems & MIDI files', included: true },
      { text: 'Early access drops', included: true },
      { text: 'Team collaboration', included: false },
      { text: 'API access', included: false },
      { text: 'White-label licensing', included: false },
      { text: 'Custom pack requests', included: false },
      { text: 'Priority support', included: false },
    ],
  },
  {
    name: 'Pro',
    monthlyPrice: 14.99,
    annualPrice: 14.99 * 10,
    description: 'For studios & power users',
    cta: 'Go Pro',
    ctaStyle: 'border border-border text-text-secondary hover:border-primary hover:text-text-primary',
    highlighted: false,
    features: [
      { text: 'Everything in Creator', included: true },
      { text: 'WAV/lossless quality', included: true },
      { text: 'Commercial license', included: true },
      { text: 'Browse all samples', included: true },
      { text: 'Stems & MIDI files', included: true },
      { text: 'Early access drops', included: true },
      { text: 'Team (5 seats)', included: true },
      { text: 'API access', included: true },
      { text: 'White-label licensing', included: true },
      { text: 'Custom pack requests', included: true },
      { text: 'Priority support', included: true },
    ],
  },
])

function formatPrice(plan: typeof plans.value[0]) {
  const price = isAnnual.value ? plan.annualPrice : plan.monthlyPrice
  if (price === 0) return '$0'
  return `$${price.toFixed(2)}`
}

function priceLabel(plan: typeof plans.value[0]) {
  if (plan.monthlyPrice === 0) return '/month'
  return isAnnual.value ? '/year' : '/month'
}

const faqs = [
  {
    question: 'Are the samples really royalty-free?',
    answer: 'Yes! Once you download a sample from SoundVault, you have a perpetual license to use it in your music, including commercial releases, sync licenses, and streaming. You never need to clear the sample or pay additional royalties.',
  },
  {
    question: 'Can I cancel my subscription anytime?',
    answer: 'Absolutely. You can cancel at any time from your account settings. Your subscription will remain active until the end of your current billing period, after which you\'ll revert to the free plan.',
  },
  {
    question: 'What\'s the difference between WAV and MP3 quality?',
    answer: 'WAV files are lossless audio at full quality (typically 44.1kHz / 24-bit), making them ideal for professional productions. MP3 files at 320kbps are smaller but slightly compressed. Free plan members get MP3; Creator and Pro members get full WAV quality.',
  },
  {
    question: 'Do unused downloads roll over?',
    answer: 'Free plan downloads reset every month and do not roll over. Creator and Pro plans have unlimited downloads, so there\'s nothing to roll over — download as much as you need, whenever you need it.',
  },
]
</script>

<template>
  <div class="min-h-screen bg-background flex flex-col">
    <Navbar />

    <main class="flex-1">
      <!-- Hero -->
      <section class="py-20 text-center px-4">
        <h1 class="font-serif text-5xl md:text-6xl text-text-primary mb-4">
          Plans &amp; Pricing
        </h1>
        <p class="text-xl font-sans text-text-secondary max-w-xl mx-auto mb-10">
          Start free. Scale as you grow. No hidden fees.
        </p>

        <!-- Annual/Monthly toggle -->
        <div class="inline-flex items-center gap-3 bg-surface border border-border rounded-xl p-1">
          <button
            class="px-5 py-2 rounded-lg text-sm font-sans font-medium transition-all duration-200"
            :class="!isAnnual ? 'bg-primary text-white shadow-glow' : 'text-text-muted hover:text-text-secondary'"
            @click="isAnnual = false"
          >
            Monthly
          </button>
          <button
            class="px-5 py-2 rounded-lg text-sm font-sans font-medium transition-all duration-200 flex items-center gap-2"
            :class="isAnnual ? 'bg-primary text-white shadow-glow' : 'text-text-muted hover:text-text-secondary'"
            @click="isAnnual = true"
          >
            Annual
            <span class="text-xs bg-success/20 text-success px-1.5 py-0.5 rounded-full">Save 17%</span>
          </button>
        </div>
      </section>

      <!-- Pricing cards -->
      <section class="max-w-6xl mx-auto px-4 sm:px-6 mb-20">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 items-stretch">
          <div
            v-for="plan in plans"
            :key="plan.name"
            class="relative bg-surface rounded-2xl p-8 flex flex-col transition-all duration-300"
            :class="plan.highlighted
              ? 'border-2 border-primary shadow-glow scale-[1.02]'
              : 'border border-border hover:border-primary/30'"
          >
            <div v-if="(plan as any).badge" class="absolute -top-3.5 left-1/2 -translate-x-1/2 bg-primary text-white text-xs font-sans font-semibold px-4 py-1 rounded-full">
              {{ (plan as any).badge }}
            </div>

            <div class="mb-8">
              <h3 class="font-sans text-xl font-semibold text-text-primary mb-1">{{ plan.name }}</h3>
              <p class="text-sm font-sans text-text-muted mb-5">{{ plan.description }}</p>
              <div class="flex items-baseline gap-1">
                <span class="font-serif text-5xl text-text-primary">{{ formatPrice(plan) }}</span>
                <span class="text-sm font-sans text-text-muted">{{ priceLabel(plan) }}</span>
              </div>
              <p v-if="isAnnual && plan.monthlyPrice > 0" class="text-xs font-sans text-success mt-1">
                (~${{ (isAnnual ? plan.annualPrice / 12 : plan.monthlyPrice).toFixed(2) }}/mo billed annually)
              </p>
            </div>

            <ul class="space-y-3 mb-8 flex-1">
              <li
                v-for="feature in plan.features"
                :key="feature.text"
                class="flex items-center gap-3 text-sm font-sans"
                :class="feature.included ? 'text-text-secondary' : 'text-text-muted/50'"
              >
                <span
                  class="flex-shrink-0 w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold"
                  :class="feature.included ? 'bg-success/20 text-success' : 'bg-surface-raised text-text-muted'"
                >
                  {{ feature.included ? '✓' : '✕' }}
                </span>
                {{ feature.text }}
              </li>
            </ul>

            <button
              class="w-full py-3.5 rounded-xl font-sans font-semibold text-sm transition-all duration-200"
              :class="plan.ctaStyle"
            >
              {{ plan.cta }}
            </button>
          </div>
        </div>
      </section>

      <!-- FAQ -->
      <section class="max-w-3xl mx-auto px-4 sm:px-6 mb-20">
        <h2 class="font-serif text-3xl text-text-primary text-center mb-10">
          Frequently asked questions
        </h2>
        <div class="space-y-3">
          <details
            v-for="faq in faqs"
            :key="faq.question"
            class="group bg-surface border border-border rounded-xl overflow-hidden"
          >
            <summary class="list-none flex items-center justify-between px-6 py-4 cursor-pointer hover:bg-surface-raised transition-colors duration-200">
              <span class="font-sans font-medium text-text-primary">{{ faq.question }}</span>
              <span class="text-text-muted group-open:rotate-180 transition-transform duration-200 flex-shrink-0 ml-4">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="6 9 12 15 18 9"/>
                </svg>
              </span>
            </summary>
            <div class="px-6 pb-5 pt-1">
              <p class="font-sans text-sm text-text-secondary leading-relaxed">{{ faq.answer }}</p>
            </div>
          </details>
        </div>
      </section>

      <!-- CTA Banner -->
      <section class="max-w-4xl mx-auto px-4 sm:px-6 mb-24">
        <div
          class="rounded-2xl p-10 text-center"
          style="background: linear-gradient(135deg, rgba(99,102,241,0.2) 0%, rgba(6,182,212,0.1) 100%); border: 1px solid rgba(99,102,241,0.3);"
        >
          <h2 class="font-serif text-3xl md:text-4xl text-text-primary mb-4">
            Ready to make better music?
          </h2>
          <p class="font-sans text-text-secondary mb-8 max-w-md mx-auto">
            Join 2 million+ producers who trust SoundVault for their royalty-free sounds.
          </p>
          <button class="px-8 py-4 bg-primary hover:bg-primary/90 text-white font-sans font-semibold text-base rounded-xl shadow-glow transition-all duration-200 hover:scale-105">
            Start for free — no credit card needed
          </button>
        </div>
      </section>
    </main>

    <Footer />
  </div>
</template>
