<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <h2 class="auth-title">Вход в систему</h2>
        <p class="auth-subtitle">Введите ваши учетные данные</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="auth-form">
        <div v-if="error" class="alert alert-danger">
          {{ error }}
        </div>
        
        <div class="form-group">
          <label for="email" class="form-label">Email</label>
          <input
            type="email"
            id="email"
            v-model="email"
            class="form-control"
            placeholder="Введите email"
            required
            :disabled="isLoading"
          />
        </div>
        
        <div class="form-group">
          <label for="password" class="form-label">Пароль</label>
          <input
            type="password"
            id="password"
            v-model="password"
            class="form-control"
            placeholder="Введите пароль"
            required
            :disabled="isLoading"
          />
        </div>
        
        <button type="submit" class="btn btn-primary btn-lg" :disabled="isLoading">
          <span v-if="isLoading">Вход...</span>
          <span v-else>Войти</span>
        </button>
        
        <div class="auth-footer">
          <p>
            Нет аккаунта? 
            <router-link to="/register" class="auth-link">
              Зарегистрироваться
            </router-link>
          </p>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store/auth'

export default {
  name: 'Login',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    
    const email = ref('')
    const password = ref('')
    const error = ref('')
    const isLoading = ref(false)
    
    // Проверяем, если пользователь уже авторизован
    onMounted(() => {
      if (authStore.isAuthenticated) {
        console.log('User already authenticated, redirecting...')
        redirectUser()
      }
    })
    
    const redirectUser = () => {
      if (authStore.isEmployee) {
        router.push('/admin')
      } else {
        router.push('/')
      }
    }
    
    const handleLogin = async () => {
      error.value = ''
      isLoading.value = true
      
      console.log('=== LOGIN DEBUG ===')
      console.log('Credentials:', {
        email: email.value,
        password: '[HIDDEN]'
      })
      
      const result = await authStore.login({
        email: email.value,
        password: password.value
      })
      
      console.log('Login result:', result)
      console.log('Store state after login:', {
        token: authStore.token,
        user: authStore.user,
        isAuthenticated: authStore.isAuthenticated
      })
      
      if (result.success) {
        console.log('Login successful! Redirecting...')
        
        // Дайте немного времени для обновления UI
        setTimeout(() => {
          if (authStore.isEmployee) {
            router.push('/admin')
          } else {
            router.push('/')
          }
        }, 100)
      } else {
        error.value = result.error || 'Ошибка авторизации'
        console.error('Login failed:', result.error)
      }
      
      isLoading.value = false
    }
    
    return {
      email,
      password,
      error,
      isLoading,
      handleLogin
    }
  }
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0a0a0a 0%, #2a2a2a 100%);
}

.auth-card {
  width: 100%;
  max-width: 400px;
  padding: 40px;
  background-color: var(--secondary-dark);
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  border: 1px solid var(--border-color);
}

.auth-header {
  text-align: center;
  margin-bottom: 30px;
}

.auth-title {
  font-size: 2rem;
  color: var(--text-light);
  margin-bottom: 10px;
  background: linear-gradient(to right, var(--accent-orange), var(--accent-purple));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.auth-subtitle {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.auth-form {
  margin-top: 30px;
}

.auth-form .btn {
  width: 100%;
  margin-top: 10px;
}

.auth-footer {
  margin-top: 20px;
  text-align: center;
  color: var(--text-muted);
}

.auth-link {
  color: var(--accent-orange);
  font-weight: 600;
}

.auth-link:hover {
  text-decoration: underline;
}
</style>