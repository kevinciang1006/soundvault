import posthog from 'posthog-js'
import type { App } from 'vue'

export function usePostHog() {
  return posthog
}

export default {
  install(app: App) {
    const key = import.meta.env.VITE_POSTHOG_KEY
    const host = import.meta.env.VITE_POSTHOG_HOST || 'https://us.i.posthog.com'

    if (!key) {
      console.warn('[PostHog] VITE_POSTHOG_KEY is not set — analytics disabled')
      return
    }

    posthog.init(key, {
      api_host: host,
      session_recording: {
        maskAllInputs: false,
      },
      capture_pageview: false, // we'll capture manually via router
    })

    app.config.globalProperties.$posthog = posthog
  },
}
