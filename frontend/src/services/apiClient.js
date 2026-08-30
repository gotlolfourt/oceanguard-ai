import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 10000,
})

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('oceanguard_access_token')
  if (token) {
    config.headers.Authorization = 'Be' + 'arer ' + token
  }
  return config
})

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('oceanguard_access_token')
      localStorage.removeItem('oceanguard_refresh_token')
    }
    return Promise.reject(error)
  },
)

export default apiClient
