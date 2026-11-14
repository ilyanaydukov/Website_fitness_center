import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authService } from '../services/auth'
import router from '../router'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user')) || null)
  const isLoading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!token.value)
  const isEmployee = computed(() => user.value?.is_employee || false)

  const login = async (credentials) => {
    try {
      isLoading.value = true
      error.value = null
      
      console.log('Sending login request with credentials:', {
        username: credentials.email,
        password: '[HIDDEN]'
      })
      
      const response = await authService.login(credentials)
      
      console.log('Login response:', response.data)
      
      // Сохраняем токен
      const accessToken = response.data.access_token
      if (accessToken) {
        token.value = accessToken
        localStorage.setItem('token', accessToken)
      }
      
      // Получаем информацию о пользователе
      await fetchUser()
      
      return { success: true }
    } catch (err) {
      console.error('Login error details:', {
        status: err.response?.status,
        data: err.response?.data,
        message: err.message
      })
      
      error.value = err.response?.data?.detail || 'Ошибка авторизации'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const fetchUser = async () => {
    try {
      if (!token.value) {
        console.log('No token available for fetching user')
        return null
      }
      
      console.log('Fetching user info...')
      const response = await authService.getCurrentUser()
      console.log('User info response:', response.data)
      
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(response.data))
      return user.value
    } catch (err) {
      console.error('Error fetching user:', {
        status: err.response?.status,
        data: err.response?.data,
        message: err.message
      })
      
      if (err.response?.status === 401) {
        // Невалидный токен - очищаем
        clearAuth()
      }
      return null
    }
  }

  const logout = () => {
    clearAuth()
    router.push('/login')
  }

  const clearAuth = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('refresh_token')
  }

  const initAuth = () => {
    const savedToken = localStorage.getItem('token')
    const savedUser = localStorage.getItem('user')
    
    if (savedToken) {
      token.value = savedToken
      if (savedUser) {
        try {
          user.value = JSON.parse(savedUser)
        } catch (e) {
          console.error('Error parsing saved user:', e)
          localStorage.removeItem('user')
        }
      }
    }
  }

  return {
    token,
    user,
    isLoading,
    error,
    isAuthenticated,
    isEmployee,
    login,
    logout,
    fetchUser,
    initAuth,
    clearAuth
  }
})