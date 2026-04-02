import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'
const TOKEN_KEY = 'price-monitor-token'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY)
  if (token) {
    config.headers = config.headers ?? {}
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const setToken = (token) => localStorage.setItem(TOKEN_KEY, token)
export const clearToken = () => localStorage.removeItem(TOKEN_KEY)
export const getToken = () => localStorage.getItem(TOKEN_KEY)
export const isAuthenticated = () => Boolean(getToken())

export const login = async ({ email, password }) => {
  const formData = new URLSearchParams()
  formData.append('username', email)
  formData.append('password', password)
  const response = await api.post('/auth/token', formData)
  return response.data
}

export const register = async (payload) => {
  const response = await api.post('/auth/register', payload)
  return response.data
}

export const fetchAnalytics = async () => {
  const response = await api.get('/analytics/summary')
  return response.data
}

export const fetchProducts = async (params = {}) => {
  const response = await api.get('/products', { params })
  return response.data
}

export const fetchProductHistory = async (id) => {
  const response = await api.get(`/products/${id}/history`)
  return response.data
}

export const refreshSource = async (source) => {
  const response = await api.post('/refresh', { source })
  return response.data
}
