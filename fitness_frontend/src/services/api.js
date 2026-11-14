// api.js
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

console.log('API URL:', API_URL)

// Создаем экземпляр axios
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 30000, // Увеличиваем таймаут для больших файлов
  withCredentials: false
})

// Интерцептор для добавления токена
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`, config.data || '')
    return config
  },
  (error) => {
    console.error('[API Request Error]', error)
    return Promise.reject(error)
  }
)

// Интерцептор для обработки ошибок
api.interceptors.response.use(
  (response) => {
    console.log(`[API Response] ${response.status} ${response.config.url}`)
    return response
  },
  async (error) => {
    console.error('[API Error]', {
      status: error.response?.status,
      url: error.config?.url,
      method: error.config?.method,
      message: error.message,
      response: error.response?.data
    })
    
    // Если ошибка 401 - разлогиниваем
    if (error.response?.status === 401) {
      console.log('Authentication error, clearing auth data')
      clearAuth()
      
      // Перенаправляем на страницу логина только если мы не на странице логина
      if (window.location.pathname !== '/login') {
        window.location.href = '/login?expired=true'
      }
    }
    
    // Для ошибок 500 показываем более понятное сообщение
    if (error.response?.status === 500) {
      console.error('Server error:', error.response.data)
      error.message = 'Серверная ошибка. Пожалуйста, попробуйте позже.'
    }
    
    // Для ошибок сети
    if (!error.response) {
      error.message = 'Ошибка сети. Проверьте подключение к интернету.'
    }
    
    return Promise.reject(error)
  }
)

// Функция для очистки аутентификации
function clearAuth() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  localStorage.removeItem('user_type')
  localStorage.removeItem('auth_store')
  
  // Очищаем заголовок авторизации
  delete api.defaults.headers.common['Authorization']
}

// Экспорт API методов
export const fitnessAPI = {
  // ============ Health check ============
  health: () => api.get('/health'),
  testConnection: () => api.get('/'),
  
  // ============ Authentication ============
  login: (data) => {
    const formData = new FormData()
    formData.append('username', data.email)
    formData.append('password', data.password)
    return api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
  },
  
  registerClient: (data) => api.post('/auth/register/client', data),
  registerEmployee: (data) => api.post('/auth/register/employee', data),
  getCurrentUser: () => api.get('/auth/me'),
  
  // ============ Users ============
  getClientInfo: () => api.get('/users/profile'),
  updateProfile: (data) => api.put('/users/profile', data),
  
  // ============ Fitness Centers (публичные) ============
  getCenters: (params) => api.get('/fitness/centers', { params }),
  getCenter: (id) => api.get(`/fitness/centers/${id}`),
  
  // ============ Rooms (публичные) ============
  getRooms: (params) => api.get('/fitness/rooms', { params }),
  getRoom: (id) => api.get(`/fitness/rooms/${id}`),
  
  // ============ Services (публичные) ============
  getServices: (params) => api.get('/fitness/services', { params }),
  getService: (id) => api.get(`/fitness/services/${id}`),
  
  // ============ Services (админка) ============
  getAdminServices: (params) => api.get('/admin/services', { params }),
  createService: (data) => api.post('/admin/services', data),
  updateService: (id, data) => api.put(`/admin/services/${id}`, data),
  deleteService: (id) => api.delete(`/admin/services/${id}`),
  
  // ============ Trainers (публичные) ============
  getTrainers: (params) => api.get('/fitness/trainers', { params }),
  getTrainer: (id) => api.get(`/fitness/trainers/${id}`),
  getTrainerFeedbacks: (trainerId) => api.get(`/fitness/trainers/${trainerId}/feedbacks`),
  createFeedback: (trainerId, data) => api.post(`/fitness/trainers/${trainerId}/feedbacks`, data),
  
  // ============ Trainers (админка) ============
  getAdminTrainers: (params) => api.get('/admin/trainers', { params }),
  createTrainer: (data) => api.post('/admin/trainers', data),
  updateTrainer: (id, data) => api.put(`/admin/trainers/${id}`, data),
  deleteTrainer: (id) => api.delete(`/admin/trainers/${id}`),
  
  // ============ Specializations ============
  getSpecializations: (params) => api.get('/admin/specializations', { params }),
  
  // ============ Workouts/Schedule (публичные) ============
  getWorkouts: (params) => api.get('/schedule/workouts', { params }),
  getWorkout: (id) => api.get(`/schedule/workouts/${id}`),
  registerForWorkout: (workoutId) => api.post(`/schedule/workouts/${workoutId}/register`),
  
  // ============ Workouts (админка) ============
  getAdminWorkouts: (params) => api.get('/admin/workouts', { params }),
  createWorkout: (data) => api.post('/schedule/workouts', data),
  updateWorkout: (id, data) => api.put(`/schedule/workouts/${id}`, data),
  deleteWorkout: (id) => api.delete(`/schedule/workouts/${id}`),
  
  // ============ Client Records ============
  getClientRecords: () => api.get('/schedule/my-registrations'),
  cancelRegistration: (recordId) => api.delete(`/schedule/registrations/${recordId}`),
  
  // ============ Subscriptions (публичные) ============
  getSubscriptions: (params) => api.get('/subscriptions', { params }),
  getSubscription: (id) => api.get(`/subscriptions/${id}`),
  getClientSubscriptions: () => api.get('/subscriptions/my-subscriptions'),
  getActiveClientSubscription: () => api.get('/subscriptions/my-active-subscription'),
  
  // ============ Subscriptions (админка) ============
  getAdminSubscriptions: (params) => api.get('/admin/subscriptions', { params }),
  createSubscription: (data) => api.post('/admin/subscriptions', data),
  updateSubscription: (id, data) => api.put(`/admin/subscriptions/${id}`, data),
  deleteSubscription: (id) => api.delete(`/admin/subscriptions/${id}`),
  
  // ============ Access Levels ============
  getAccessLevels: (params) => api.get('/subscriptions/access-levels', { params }),
  
  // ============ Reports ============
  generateEquipmentPDF: (roomId) => 
    api.get(`/admin/pdf/equipment/${roomId}`, { 
      responseType: 'blob',
      headers: {
        'Accept': 'application/pdf'
      }
    }),
    
  generateSchedulePDF: (dateFrom, dateTo) => 
    api.get(`/admin/pdf/schedule/${dateFrom}/${dateTo}`, { 
      responseType: 'blob',
      headers: {
        'Accept': 'application/pdf'
      }
    }),
    
  generateRegistrationsPDF: (workoutId) => 
    api.get(`/admin/pdf/registrations/${workoutId}`, { 
      responseType: 'blob',
      headers: {
        'Accept': 'application/pdf'
      }
    }),
  
  // ============ Equipment ============
  getEquipmentByRoom: (roomId) => api.get(`/admin/equipment/${roomId}`),
  
  // ============ Admin Statistics ============
  getAdminStats: () => api.get('/admin/stats'),
  
  // ============ Admin Employees ============
  getEmployees: (params) => api.get('/admin/employees', { params }),
  getEmployee: (id) => api.get(`/admin/employees/${id}`),
  createEmployee: (data) => api.post('/admin/employees', data),
  updateEmployee: (id, data) => api.put(`/admin/employees/${id}`, data),
  deleteEmployee: (id) => api.delete(`/admin/employees/${id}`),
  
  // ============ Admin Positions ============
  getPositions: (params) => api.get('/admin/positions', { params }),
  createPosition: (data) => api.post('/admin/positions', data),
  updatePosition: (id, data) => api.put(`/admin/positions/${id}`, data),
  deletePosition: (id) => api.delete(`/admin/positions/${id}`),
  
  // ============ Client Subscriptions Management ============
  createClientSubscription: (data) => api.post('/client-subscriptions', data),
  updateClientSubscription: (id, data) => api.put(`/client-subscriptions/${id}`, data),
  deleteClientSubscription: (id) => api.delete(`/client-subscriptions/${id}`),
  getClientSubscription: (id) => api.get(`/client-subscriptions/${id}`)
}

// Экспортируем базовый экземпляр axios для кастомных запросов
export default api

// Вспомогательная функция для скачивания файлов
export const downloadFile = (blob, filename) => {
  try {
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    return true
  } catch (error) {
    console.error('Error downloading file:', error)
    throw error
  }
}

// Вспомогательная функция для проверки статуса подключения
export const checkConnection = async () => {
  try {
    const response = await api.get('/health')
    return {
      connected: true,
      status: response.status,
      data: response.data
    }
  } catch (error) {
    return {
      connected: false,
      error: error.message
    }
  }
}

// Вспомогательная функция для обработки ошибок
export const handleApiError = (error, defaultMessage = 'Произошла ошибка') => {
  if (error.response?.data?.detail) {
    return error.response.data.detail
  }
  
  if (error.response?.data?.message) {
    return error.response.data.message
  }
  
  if (error.message) {
    return error.message
  }
  
  return defaultMessage
}