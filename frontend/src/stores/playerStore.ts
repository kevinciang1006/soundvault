import { defineStore } from 'pinia'
import { ref } from 'vue'
import apiClient from '@/api/client'
import { usePostHog } from '@/plugins/posthog'
import type { Sample } from '@/types'

const KEY_FREQUENCIES: Record<string, number> = {
  'C': 523, 'C#': 554, 'D': 587, 'D#': 622, 'E': 659,
  'F': 698, 'F#': 740, 'G': 784, 'G#': 831, 'A': 440, 'A#': 466, 'B': 494,
  'Cm': 523, 'C#m': 554, 'Dm': 587, 'D#m': 622, 'Em': 659,
  'Fm': 698, 'F#m': 740, 'Gm': 784, 'G#m': 831, 'Am': 440, 'A#m': 466, 'Bm': 494,
}

export const usePlayerStore = defineStore('player', () => {
  const currentSample = ref<Sample | null>(null)
  const isPlaying = ref(false)
  const queue = ref<Sample[]>([])
  const currentIndex = ref(0)
  const volume = ref(0.7)

  let audioContext: AudioContext | null = null
  let gainNode: GainNode | null = null
  let oscillator: OscillatorNode | null = null
  let playTimeout: ReturnType<typeof setTimeout> | null = null

  function getAudioContext(): AudioContext {
    if (!audioContext) {
      audioContext = new AudioContext()
    }
    return audioContext
  }

  function stopCurrentAudio() {
    if (playTimeout) {
      clearTimeout(playTimeout)
      playTimeout = null
    }
    if (oscillator) {
      try {
        oscillator.stop()
      } catch (_) {
        // already stopped
      }
      oscillator = null
    }
    if (gainNode) {
      gainNode = null
    }
  }

  function playTone(sample: Sample) {
    stopCurrentAudio()

    const ctx = getAudioContext()
    const frequency = KEY_FREQUENCIES[sample.key] ?? 440
    const duration = Math.min(sample.duration_seconds, 3)

    gainNode = ctx.createGain()
    gainNode.connect(ctx.destination)
    gainNode.gain.setValueAtTime(0, ctx.currentTime)
    gainNode.gain.linearRampToValueAtTime(volume.value, ctx.currentTime + 0.1)
    gainNode.gain.setValueAtTime(volume.value, ctx.currentTime + duration - 0.3)
    gainNode.gain.linearRampToValueAtTime(0, ctx.currentTime + duration)

    oscillator = ctx.createOscillator()
    oscillator.type = sample.sample_type === 'loop' ? 'sine' : 'triangle'
    oscillator.frequency.setValueAtTime(frequency, ctx.currentTime)
    oscillator.connect(gainNode)
    oscillator.start(ctx.currentTime)
    oscillator.stop(ctx.currentTime + duration)

    oscillator.onended = () => {
      isPlaying.value = false
    }

    playTimeout = setTimeout(() => {
      isPlaying.value = false
    }, duration * 1000 + 100)
  }

  async function play(sample: Sample) {
    stopCurrentAudio()
    currentSample.value = sample
    isPlaying.value = true

    // Track in queue if not already present
    if (!queue.value.find(s => s.id === sample.id)) {
      queue.value.push(sample)
      currentIndex.value = queue.value.length - 1
    } else {
      currentIndex.value = queue.value.findIndex(s => s.id === sample.id)
    }

    playTone(sample)

    usePostHog().capture('sample_played', {
      sample_id: sample.id,
      sample_name: sample.filename,
      sample_key: sample.key,
      sample_bpm: sample.bpm,
      sample_type: sample.sample_type,
    })

    // Notify backend
    try {
      await apiClient.post(`/api/samples/${sample.id}/play`)
    } catch (_) {
      // Non-critical
    }
  }

  function pause() {
    isPlaying.value = false
    stopCurrentAudio()
  }

  function resume() {
    if (currentSample.value) {
      isPlaying.value = true
      playTone(currentSample.value)
    }
  }

  function next() {
    if (queue.value.length === 0) return
    const nextIndex = (currentIndex.value + 1) % queue.value.length
    currentIndex.value = nextIndex
    play(queue.value[nextIndex])
  }

  function prev() {
    if (queue.value.length === 0) return
    const prevIndex = (currentIndex.value - 1 + queue.value.length) % queue.value.length
    currentIndex.value = prevIndex
    play(queue.value[prevIndex])
  }

  function setVolume(v: number) {
    volume.value = Math.max(0, Math.min(1, v))
    if (gainNode && audioContext) {
      gainNode.gain.setValueAtTime(volume.value, audioContext.currentTime)
    }
  }

  function addToQueue(sample: Sample) {
    if (!queue.value.find(s => s.id === sample.id)) {
      queue.value.push(sample)
    }
  }

  function setQueue(samples: Sample[], startIndex: number = 0) {
    queue.value = samples
    currentIndex.value = startIndex
    if (samples[startIndex]) {
      play(samples[startIndex])
    }
  }

  return {
    currentSample,
    isPlaying,
    queue,
    currentIndex,
    volume,
    play,
    pause,
    resume,
    next,
    prev,
    setVolume,
    addToQueue,
    setQueue,
  }
})
