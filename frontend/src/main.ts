import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import posthogPlugin, { usePostHog } from './plugins/posthog'
import './style.css'

const app = createApp(App)
app.use(createPinia())
app.use(posthogPlugin)
app.use(router)

// Track page views on route change
router.afterEach((to) => {
  const posthog = usePostHog()
  posthog.capture('$pageview', { path: to.fullPath })
})

app.mount('#app')
