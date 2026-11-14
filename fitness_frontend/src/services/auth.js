import api from './api'

export const authService = {
  login: (credentials) => 
    api.post('/auth/login', new URLSearchParams({
      username: credentials.email,  // Передаем email в поле username
      password: credentials.password,
      grant_type: 'password'
    }), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }),
  
  registerClient: (userData) => 
    api.post('/auth/register/client', userData),
  
  registerEmployee: (userData) => 
    api.post('/auth/register/employee', userData),
  
  getCurrentUser: () => 
    api.get('/auth/me'),
  
  logout: () => {
    localStorage.removeItem('token')
  },
  
  // Дополнительные методы
  refreshToken: () => 
    api.post('/auth/refresh'),
  
  changePassword: (data) =>
    api.post('/auth/change-password', data),
  
  resetPassword: (email) =>
    api.post('/auth/reset-password', { email }),
  
  verifyEmail: (token) =>
    api.post('/auth/verify-email', { token })
}