<script setup lang="ts">
import Navbar from '@/components/layout/Navbar.vue'
import Footer from '@/components/layout/Footer.vue'
import HeroSection from '@/components/landing/HeroSection.vue'
import SamplePreviewStrip from '@/components/landing/SamplePreviewStrip.vue'
import FeaturesSection from '@/components/landing/FeaturesSection.vue'
import PricingCards from '@/components/landing/PricingCards.vue'
</script>

<template>
  <div class="min-h-screen bg-background flex flex-col">
    <Navbar />
    <main class="flex-1">
      <HeroSection />
      <SamplePreviewStrip />
      <FeaturesSection />
      <PricingCards />
    </main>
    <Footer />
  </div>
</template>
