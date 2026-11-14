<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <h2 class="auth-title">Регистрация</h2>
        <p class="auth-subtitle">Создайте новый аккаунт</p>
      </div>
      
      <form @submit.prevent="handleRegister" class="auth-form">
        <div v-if="error" class="alert alert-danger">
          {{ error }}
        </div>
        
        <div class="row">
          <div class="col">
            <div class="form-group">
              <label for="firstName" class="form-label">Имя</label>
              <input
                type="text"
                id="firstName"
                v-model="formData.first_name"
                class="form-control"
                placeholder="Введите имя"
                required
                :disabled="isLoading"
              />
            </div>
          </div>
          <div class="col">
            <div class="form-group">
              <label for="lastName" class="form-label">Фамилия</label>
              <input
                type="text"
                id="lastName"
                v-model="formData.last_name"
                class="form-control"
                placeholder="Введите фамилию"
                required
                :disabled="isLoading"
              />
            </div>
          </div>
        </div>
        
        <div class="form-group">
          <label for="email" class="form-label">Email</label>
          <input
            type="email"
            id="email"
            v-model="formData.email"
            class="form-control"
            placeholder="Введите email"
            required
            :disabled="isLoading"
          />
        </div>
        
        <div class="form-group">
          <label for="phone" class="form-label">Телефон</label>
          <input
            type="tel"
            id="phone"
            v-model="formData.phone"
            class="form-control"
            placeholder="+7 (XXX) XXX-XX-XX"
            :disabled="isLoading"
          />
        </div>
        
        <div class="row">
          <div class="col">
            <div class="form-group">
              <label for="password" class="form-label">Пароль</label>
              <input
                type="password"
                id="password"
                v-model="formData.password"
                class="form-control"
                placeholder="Введите пароль"
                required
                :disabled="isLoading"
              />
            </div>
          </div>
          <div class="col">
            <div class="form-group">
              <label for="confirmPassword" class="form-label">Подтверждение пароля</label>
              <input
                type="password"
                id="confirmPassword"
                v-model="confirmPassword"
                class="form-control"
                placeholder="Повторите пароль"
                required
                :disabled="isLoading"
              />
            </div>
          </div>
        </div>
        
        <div class="form-group">
          <label for="dateOfBirth" class="form-label">Дата рождения</label>
          <input
            type="date"
            id="dateOfBirth"
            v-model="formData.date_of_birth"
            class="form-control"
            :disabled="isLoading"
          />
        </div>
        
        <button type="submit" class="btn btn-primary btn-lg" :disabled="isLoading">
          <span v-if="isLoading">Регистрация...</span>
          <span v-else>Зарегистрироваться</span>
        </button>
        
        <div class="auth-footer">
          <p>
            Уже есть аккаунт? 
            <router-link to="/login" class="auth-link">
              Войти
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
  name: 'Register',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    
    const formData = ref({
      first_name: '',
      last_name: '',
      email: '',
      phone: '',
      password: '',
      date_of_birth: ''
    })
    
    const confirmPassword = ref('')
    const error = ref('')
    const isLoading = ref(false)
    
    // Проверяем, если пользователь уже авторизован
    onMounted(() => {
      if (authStore.isAuthenticated) {
        router.push('/')
      }
    })
    
    const handleRegister = async () => {
      if (formData.value.password !== confirmPassword.value) {
        error.value = 'Пароли не совпадают'
        return
      }
      
      if (formData.value.password.length < 6) {
        error.value = 'Пароль должен содержать минимум 6 символов'
        return
      }
      
      error.value = ''
      isLoading.value = true
      
      const result = await authStore.register(formData.value)
      
      if (result.success) {
        alert('Регистрация успешна!')
        router.push('/')
      } else {
        error.value = result.error
      }
      
      isLoading.value = false
    }
    
    return {
      formData,
      confirmPassword,
      error,
      isLoading,
      handleRegister
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
  max-width: 500px;
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
  margin-top: 20px;
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