import apiClient from './apiClient'

export const authService = {
  async login(email, password) {
    const response = await apiClient.post('/api/v1/auth/login', { email, password })
    return response.data.data
  },
  async register(payload) {
    const response = await apiClient.post('/api/v1/auth/register', payload)
    return response.data.data
  },
  async getCurrentUser() {
    const response = await apiClient.get('/api/v1/users/me')
    return response.data.data
  },
}
