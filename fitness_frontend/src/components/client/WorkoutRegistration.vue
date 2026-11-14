<template>
  <div class="container">
    <div v-if="isLoading" class="loader"></div>
    
    <div v-else-if="error" class="error-container">
      <div class="alert alert-danger">
        {{ error }}
      </div>
      <router-link to="/schedule" class="btn btn-primary">
        Вернуться к расписанию
      </router-link>
    </div>
    
    <div v-else-if="workout" class="workout-registration">
      <div class="registration-header">
        <h1 class="page-title">Запись на тренировку</h1>
        <button @click="$router.back()" class="btn btn-secondary">
          ← Назад
        </button>
      </div>
      
      <div class="workout-details card">
        <h2>{{ workout.service?.name || 'Тренировка' }}</h2>
        
        <div class="details-grid">
          <div class="detail-item">
            <strong>Дата:</strong> {{ formatDate(workout.workout_date) }}
          </div>
          <div class="detail-item">
            <strong>Время:</strong> {{ workout.start_time }} - {{ workout.end_time }}
          </div>
          <div class="detail-item">
            <strong>Тренер:</strong> {{ workout.trainer?.first_name }} {{ workout.trainer?.last_name }}
          </div>
          <div class="detail-item">
            <strong>Зал:</strong> {{ workout.room?.name }}
          </div>
          <div class="detail-item">
            <strong>Макс. участников:</strong> {{ workout.max_persons_capacity }}
          </div>
          <div class="detail-item">
            <strong>Записано:</strong> {{ workout.current_number_of_recorded }}
          </div>
        </div>
        
        <div class="capacity-indicator">
          <div class="capacity-bar">
            <div 
              class="capacity-fill" 
              :style="{ width: capacityPercentage + '%' }"
              :class="{ 'full': isFull }"
            ></div>
          </div>
          <div class="capacity-text">
            <span v-if="isFull" class="text-danger">Мест нет</span>
            <span v-else>Свободно мест: {{ freeSpots }}</span>
          </div>
        </div>
        
        <div v-if="workout.service?.description" class="service-description">
          <h4>Описание услуги:</h4>
          <p>{{ workout.service.description }}</p>
        </div>
        
        <div v-if="workout.trainer" class="trainer-info">
          <h4>Информация о тренере:</h4>
          <p><strong>Опыт работы:</strong> {{ workout.trainer.work_experience || 'Не указан' }} лет</p>
          <p><strong>Специализация:</strong> {{ workout.trainer.specialization?.name || 'Не указана' }}</p>
        </div>
        
        <div class="registration-form">
          <h3>Подтверждение записи</h3>
          
          <div v-if="isRegistered" class="alert alert-success">
            Вы уже записаны на эту тренировку!
          </div>
          
          <div v-else-if="isFull" class="alert alert-warning">
            К сожалению, все места на эту тренировку заняты.
          </div>
          
          <div v-else class="form-actions">
            <button @click="register" class="btn btn-primary btn-lg" :disabled="isRegistering">
              {{ isRegistering ? 'Запись...' : 'Записаться' }}
            </button>
          </div>
          
          <div v-if="isRegistered" class="existing-registration">
            <button @click="cancelRegistration" class="btn btn-danger">
              Отменить запись
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { format } from 'date-fns'
import { fitnessAPI } from '../../services/api'

export default {
  name: 'WorkoutRegistration',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const workout = ref(null)
    const isLoading = ref(false)
    const isRegistering = ref(false)
    const error = ref('')
    const isRegistered = ref(false)
    const registrationId = ref(null)
    
    const workoutId = route.params.id
    
    const fetchWorkout = async () => {
      isLoading.value = true
      try {
        const [workoutRes, recordsRes] = await Promise.all([
          fitnessAPI.getWorkout(workoutId),
          fitnessAPI.getClientRecords()
        ])
        
        workout.value = workoutRes.data
        
        // Проверяем, записан ли уже пользователь
        const userRecord = recordsRes.data.find(record => 
          record.workout_id === parseInt(workoutId)
        )
        
        if (userRecord) {
          isRegistered.value = true
          registrationId.value = userRecord.id
        }
      } catch (error) {
        console.error('Error fetching workout:', error)
        error.value = 'Тренировка не найдена'
      } finally {
        isLoading.value = false
      }
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return ''
      return format(new Date(dateString), 'dd.MM.yyyy')
    }
    
    const isFull = computed(() => {
      if (!workout.value) return false
      return workout.value.current_number_of_recorded >= workout.value.max_persons_capacity
    })
    
    const freeSpots = computed(() => {
      if (!workout.value) return 0
      return workout.value.max_persons_capacity - workout.value.current_number_of_recorded
    })
    
    const capacityPercentage = computed(() => {
      if (!workout.value || workout.value.max_persons_capacity === 0) return 0
      return (workout.value.current_number_of_recorded / workout.value.max_persons_capacity) * 100
    })
    
    const register = async () => {
      if (isFull.value) {
        alert('Все места заняты')
        return
      }
      
      isRegistering.value = true
      try {
        await fitnessAPI.registerForWorkout(workoutId)
        alert('Вы успешно записались на тренировку!')
        fetchWorkout()
      } catch (error) {
        alert(error.response?.data?.detail || 'Ошибка записи')
      } finally {
        isRegistering.value = false
      }
    }
    
    const cancelRegistration = async () => {
      if (!confirm('Вы уверены, что хотите отменить запись?')) return
      
      try {
        await fitnessAPI.cancelRegistration(registrationId.value)
        alert('Запись отменена')
        fetchWorkout()
      } catch (error) {
        alert(error.response?.data?.detail || 'Ошибка отмены записи')
      }
    }
    
    onMounted(() => {
      if (!workoutId) {
        error.value = 'ID тренировки не указан'
        return
      }
      fetchWorkout()
    })
    
    return {
      workout,
      isLoading,
      isRegistering,
      error,
      isRegistered,
      formatDate,
      isFull,
      freeSpots,
      capacityPercentage,
      register,
      cancelRegistration
    }
  }
}
</script>

<style scoped>
.registration-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.workout-details {
  padding: 30px;
}

.workout-details h2 {
  color: var(--accent-orange);
  margin-bottom: 20px;
  text-align: center;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin: 20px 0;
  padding: 20px;
  background-color: var(--primary-dark);
  border-radius: var(--radius);
}

.detail-item {
  padding: 10px;
}

.capacity-indicator {
  margin: 30px 0;
}

.capacity-bar {
  height: 20px;
  background-color: var(--border-color);
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 10px;
}

.capacity-fill {
  height: 100%;
  background: linear-gradient(to right, var(--accent-orange), var(--accent-purple));
  transition: width 0.3s ease;
}

.capacity-fill.full {
  background: linear-gradient(to right, var(--danger), #ff6b6b);
}

.capacity-text {
  text-align: center;
  font-weight: 600;
}

.service-description,
.trainer-info {
  margin: 20px 0;
  padding: 15px;
  background-color: var(--primary-dark);
  border-radius: var(--radius);
}

.service-description h4,
.trainer-info h4 {
  color: var(--accent-orange);
  margin-bottom: 10px;
}

.registration-form {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid var(--border-color);
  text-align: center;
}

.registration-form h3 {
  margin-bottom: 20px;
}

.form-actions {
  margin: 20px 0;
}

.existing-registration {
  margin-top: 20px;
}

.error-container {
  text-align: center;
  padding: 50px;
}

.error-container .alert {
  margin-bottom: 30px;
}
</style>