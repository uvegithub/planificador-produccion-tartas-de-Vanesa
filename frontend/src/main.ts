import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { clerkPlugin } from '@clerk/vue'

const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY

if (!PUBLISHABLE_KEY) {
  throw new Error('Añade tu Clerk Publishable Key al archivo .env.local')
}

const app = createApp(App)

app.use(clerkPlugin, { publishableKey: PUBLISHABLE_KEY })


app.mount('#app')
