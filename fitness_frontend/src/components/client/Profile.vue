<template>
  <div class="container">
    <h1 class="page-title">Мой профиль</h1>
    
    <div class="profile-grid">
      <!-- Информация профиля -->
      <div class="card">
        <div class="card-header">
          <h3>Основная информация</h3>
        </div>
        <div class="card-body">
          <form @submit.prevent="updateProfile" class="profile-form">
            <div class="row">
              <div class="col">
                <div class="form-group">
                  <label class="form-label">Имя</label>
                  <input type="text" v-model="profileForm.first_name" class="form-control" required />
                </div>
              </div>
              <div class="col">
                <div class="form-group">
                  <label class="form-label">Фамилия</label>
                  <input type="text" v-model="profileForm.last_name" class="form-control" required />
                </div>
              </div>
            </div>
            
            <div class="form-group">
              <label class="form-label">Email</label>
              <input type="email" v-model="profileForm.email" class="form-control" disabled />
              <small class="form-text">Email нельзя изменить</small>
            </div>
            
            <div class="form-group">
              <label class="form-label">Телефон</label>
              <input type="tel" v-model="profileForm.phone" class="form-control" />
            </div>
            
            <div class="form-group">
              <label class="form-label">Дата рождения</label>
              <input type="date" v-model="profileForm.date_of_birth" class="form-control" />
            </div>
            
            <div class="form-group">
              <label class="form-label">Дата регистрации</label>
              <input type="text" :value="formatDate(profileForm.registration_date)" class="form-control" disabled />
            </div>
            
            <button type="submit" class="btn btn-primary" :disabled="isSaving">
              {{ isSaving ? 'Сохранение...' : 'Сохранить изменения' }}
            </button>
          </form>
        </div>
      </div>
      
      <!-- Изменение пароля -->
      <div class="card">
        <div class="card-header">
          <h3>Безопасность</h3>
        </div>
        <div class="card-body">
          <form @submit.prevent="changePassword" class="password-form">
            <div class="form-group">
              <label class="form-label">Текущий пароль</label>
              <input type="password" v-model="passwordForm.currentPassword" class="form-control" required />
            </div>
            
            <div class="row">
              <div class="col">
                <div class="form-group">
                  <label class="form-label">Новый пароль</label>
                  <input type="password" v-model="passwordForm.newPassword" class="form-control" required />
                </div>
              </div>
              <div class="col">
                <div class="form-group">
                  <label class="form-label">Подтверждение</label>
                  <input type="password" v-model="passwordForm.confirmPassword" class="form-control" required />
                </div>
              </div>
            </div>
            
            <div v-if="passwordError" class="alert alert-danger">
              {{ passwordError }}
            </div>
            
            <button type="submit" class="btn btn-primary" :disabled="isChangingPassword">
              {{ isChangingPassword ? 'Изменение...' : 'Изменить пароль' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { format } from 'date-fns'
import { fitnessAPI } from '../../services/api'

export default {
  name: 'Profile',
  setup() {
    const profileForm = ref({
      first_name: '',
      last_name: '',
      email: '',
      phone: '',
      date_of_birth: '',
      registration_date: ''
    })
    
    const passwordForm = ref({
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    })
    
    const isSaving = ref(false)
    const isChangingPassword = ref(false)
    const passwordError = ref('')
    
    const fetchProfile = async () => {
      try {
        const response = await fitnessAPI.getClientInfo()
        Object.assign(profileForm.value, response.data)
      } catch (error) {
        console.error('Error fetching profile:', error)
      }
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return ''
      return format(new Date(dateString), 'dd.MM.yyyy')
    }
    
    const updateProfile = async () => {
      isSaving.value = true
      try {
        await fitnessAPI.updateProfile(profileForm.value)
        alert('Профиль успешно обновлен!')
      } catch (error) {
        alert(error.response?.data?.detail || 'Ошибка обновления профиля')
      } finally {
        isSaving.value = false
      }
    }
    
    const changePassword = async () => {
      if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
        passwordError.value = 'Пароли не совпадают'
        return
      }
      
      if (passwordForm.value.newPassword.length < 6) {
        passwordError.value = 'Пароль должен содержать минимум 6 символов'
        return
      }
      
      isChangingPassword.value = true
      passwordError.value = ''
      
      try {
        await fitnessAPI.updateProfile({
          password: passwordForm.value.newPassword
        })
        
        alert('Пароль успешно изменен!')
        passwordForm.value = {
          currentPassword: '',
          newPassword: '',
          confirmPassword: ''
        }
      } catch (error) {
        passwordError.value = error.response?.data?.detail || 'Ошибка изменения пароля'
      } finally {
        isChangingPassword.value = false
      }
    }
    
    onMounted(() => {
      fetchProfile()
    })
    
    return {
      profileForm,
      passwordForm,
      isSaving,
      isChangingPassword,
      passwordError,
      formatDate,
      updateProfile,
      changePassword
    }
  }
}
</script>

<style scoped>
.profile-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 30px;
}

@media (min-width: 992px) {
  .profile-grid {
    grid-template-columns: 2fr 1fr;
  }
}

.profile-form .btn,
.password-form .btn {
  margin-top: 20px;
}

.form-text {
  color: var(--text-muted);
  font-size: 0.85rem;
  margin-top: 5px;
}
</style>