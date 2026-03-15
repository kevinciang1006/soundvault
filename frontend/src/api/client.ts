import axios from 'axios'

// Create axios instance with configurable base URL
// In production, VITE_API_URL will be set by the build process
// In development, it falls back to localhost:8000
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

export default apiClient
