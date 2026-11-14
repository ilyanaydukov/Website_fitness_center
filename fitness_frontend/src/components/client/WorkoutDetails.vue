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
    
    <div v-else-if="workout" class="workout-details-page">
      <div class="workout-header">
        <h1 class="page-title">{{ workout.service?.name || 'Тренировка' }}</h1>
        <button @click="$router.back()" class="btn btn-secondary">
          ← Назад
        </button>
      </div>
      
      <div class="workout-content">
        <div class="main-info card">
          <div class="workout-meta">
            <div class="meta-item">
              <span class="meta-label">Дата:</span>
              <span class="meta-value">{{ formatDate(workout.workout_date) }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Время:</span>
              <span class="meta-value">{{ workout.start_time }} - {{ workout.end_time }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Длительность:</span>
              <span class="meta-value">{{ calculateDuration() }} минут</span>
            </div>
          </div>
          
          <div class="capacity-info">
            <div class="capacity-bar">
              <div 
                class="capacity-fill" 
                :style="{ width: capacityPercentage + '%' }"
                :class="{ 'full': isFull }"
              ></div>
            </div>
            <div class="capacity-text">
              <span v-if="isFull" class="text-danger">
                <strong>Мест нет</strong> ({{ workout.current_number_of_recorded }}/{{ workout.max_persons_capacity }})
              </span>
              <span v-else>
                <strong>Свободно мест:</strong> {{ freeSpots }} ({{ workout.current_number_of_recorded }}/{{ workout.max_persons_capacity }})
              </span>
            </div>
          </div>
        </div>
        
        <div class="grid">
          <!-- Информация о тренере -->
          <div class="card trainer-card">
            <h3 class="card-title">Тренер</h3>
            <div class="trainer-info">
              <div class="trainer-name">
                <h4>{{ workout.trainer?.first_name }} {{ workout.trainer?.last_name }}</h4>
                <span class="specialization">{{ workout.trainer?.specialization?.name }}</span>
              </div>
              <div class="trainer-details">
                <p v-if="workout.trainer?.work_experience">
                  <strong>Опыт:</strong> {{ workout.trainer.work_experience }} лет
                </p>
                <p v-if="workout.trainer?.specialization?.description">
                  {{ workout.trainer.specialization.description }}
                </p>
              </div>
              <div class="trainer-actions">
                <button @click="viewTrainerProfile" class="btn btn-secondary">
                  Профиль тренера
                </button>
                <button 
                  v-if="isAuthenticated && !isEmployee"
                  @click="leaveFeedback"
                  class="btn btn-warning"
                >
                  Оставить отзыв
                </button>
              </div>
            </div>
          </div>
          
          <!-- Информация о зале -->
          <div class="card room-card">
            <h3 class="card-title">Зал</h3>
            <div class="room-info">
              <h4>{{ workout.room?.name }}</h4>
              <p v-if="workout.room?.description">{{ workout.room.description }}</p>
              <p><strong>Вместимость:</strong> {{ workout.room?.capacity || workout.max_persons_capacity }} человек</p>
              <p v-if="workout.room?.equipment">
                <strong>Оборудование:</strong> {{ workout.room.equipment }}
              </p>
            </div>
          </div>
          
          <!-- Информация об услуге -->
          <div class="card service-card">
            <h3 class="card-title">Услуга</h3>
            <div class="service-info">
              <h4>{{ workout.service?.name }}</h4>
              <p v-if="workout.service?.description">{{ workout.service.description }}</p>
              <div class="service-meta">
                <p v-if="workout.service?.price">
                  <strong>Стоимость:</strong> {{ workout.service.price }} ₽
                </p>
                <p v-if="workout.service?.duration">
                  <strong>Длительность:</strong> {{ workout.service.duration }} минут
                </p>
              </div>
            </div>
          </div>
          
          <!-- Запись на тренировку -->
          <div class="card registration-card">
            <h3 class="card-title">Запись</h3>
            <div class="registration-info">
              <div v-if="isRegistered" class="alert alert-success">
                <p>Вы записаны на эту тренировку!</p>
                <small>ID записи: {{ registrationId }}</small>
              </div>
              
              <div v-else-if="isFull" class="alert alert-warning">
                <p>К сожалению, все места заняты</p>
                <small>Попробуйте найти другую тренировку</small>
              </div>
              
              <div v-else-if="!isAuthenticated" class="alert alert-info">
                <p>Для записи необходимо войти в систему</p>
                <router-link to="/login" class="btn btn-sm btn-primary">
                  Войти
                </router-link>
              </div>
              
              <div v-else-if="isEmployee" class="alert alert-info">
                <p>Администраторы не могут записываться на тренировки</p>
              </div>
              
              <div v-else class="registration-actions">
                <button @click="register" class="btn btn-primary btn-lg" :disabled="isRegistering">
                  {{ isRegistering ? 'Запись...' : 'Записаться' }}
                </button>
                <p class="hint">
                  После записи вы получите подтверждение на email
                </p>
              </div>
              
              <div v-if="isRegistered" class="existing-registration">
                <button @click="cancelRegistration" class="btn btn-danger">
                  Отменить запись
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Дополнительная информация -->
        <div class="additional-info">
          <div class="card">
            <h3>Дополнительная информация</h3>
            <div class="additional-details">
              <div v-if="workout.notes">
                <h4>Примечания:</h4>
                <p>{{ workout.notes }}</p>
              </div>
              <div v-if="workout.requirements">
                <h4>Требования:</h4>
                <p>{{ workout.requirements }}</p>
              </div>
              <div v-if="workout.equipment_needed">
                <h4>Необходимое оборудование:</h4>
                <p>{{ workout.equipment_needed }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Похожие тренировки -->
        <div class="similar-workouts" v-if="similarWorkouts.length > 0">
          <h3>Похожие тренировки</h3>
          <div class="similar-grid">
            <div v-for="similar in similarWorkouts" :key="similar.id" class="card similar-card">
              <h4>{{ similar.service?.name }}</h4>
              <p>{{ formatDate(similar.workout_date) }} {{ similar.start_time }}</p>
              <p>{{ similar.trainer?.first_name }} {{ similar.trainer?.last_name }}</p>
              <button @click="viewWorkout(similar.id)" class="btn btn-sm btn-primary">
                Подробнее
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { format, differenceInMinutes, parseISO } from 'date-fns'
import { fitnessAPI } from '../../services/api'
import { useAuthStore } from '../../store/auth'

export default {
  name: 'WorkoutDetails',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const authStore = useAuthStore()
    
    const workout = ref(null)
    const similarWorkouts = ref([])
    const isLoading = ref(false)
    const isRegistering = ref(false)
    const error = ref('')
    const isRegistered = ref(false)
    const registrationId = ref(null)
    
    const workoutId = route.params.id
    
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const isEmployee = computed(() => authStore.isEmployee)
    
    const fetchWorkout = async () => {
      isLoading.value = true
      try {
        const [workoutRes, recordsRes, similarRes] = await Promise.all([
          fitnessAPI.getWorkout(workoutId),
          fitnessAPI.getClientRecords(),
          fitnessAPI.getSimilarWorkouts(workoutId)
        ])
        
        workout.value = workoutRes.data
        similarWorkouts.value = similarRes.data || []
        
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
    
    const calculateDuration = () => {
      if (!workout.value?.start_time || !workout.value?.end_time) return 60
      
      const start = parseISO(`2000-01-01T${workout.value.start_time}`)
      const end = parseISO(`2000-01-01T${workout.value.end_time}`)
      return differenceInMinutes(end, start)
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
    
    const viewTrainerProfile = () => {
      if (workout.value?.trainer?.id) {
        router.push(`/trainers/${workout.value.trainer.id}`)
      }
    }
    
    const leaveFeedback = () => {
      if (workout.value?.trainer?.id) {
        router.push(`/feedback/${workout.value.trainer.id}`)
      }
    }
    
    const viewWorkout = (id) => {
      router.push(`/workout/${id}`)
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
      similarWorkouts,
      isLoading,
      isRegistering,
      error,
      isRegistered,
      registrationId,
      isAuthenticated,
      isEmployee,
      formatDate,
      calculateDuration,
      isFull,
      freeSpots,
      capacityPercentage,
      register,
      cancelRegistration,
      viewTrainerProfile,
      leaveFeedback,
      viewWorkout
    }
  }
}
</script>

<style scoped>
.workout-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.workout-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.main-info {
  padding: 20px;
  background: linear-gradient(135deg, var(--primary-dark) 0%, #2a2a2a 100%);
}

.workout-meta {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.meta-item {
  padding: 15px;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: var(--radius);
}

.meta-label {
  display: block;
  color: var(--accent-orange);
  font-weight: 600;
  margin-bottom: 5px;
}

.meta-value {
  color: var(--text-light);
  font-size: 1.1rem;
}

.capacity-info {
  margin-top: 20px;
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
  font-size: 1.1rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.card-title {
  color: var(--accent-orange);
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border-color);
}

.trainer-card .trainer-info {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.trainer-name {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.trainer-name h4 {
  margin: 0;
  color: var(--text-light);
}

.specialization {
  background: linear-gradient(135deg, var(--accent-orange), var(--accent-purple));
  color: white;
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 0.8rem;
  align-self: flex-start;
}

.trainer-details p {
  margin: 5px 0;
  color: var(--text-muted);
}

.trainer-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.room-card .room-info,
.service-card .service-info {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.room-info h4,
.service-info h4 {
  color: var(--text-light);
  margin: 0;
}

.service-meta {
  margin-top: 10px;
  padding: 10px;
  background-color: var(--primary-dark);
  border-radius: var(--radius);
}

.registration-card .registration-info {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.registration-actions {
  text-align: center;
}

.hint {
  margin-top: 10px;
  color: var(--text-muted);
  font-size: 0.9rem;
}

.existing-registration {
  text-align: center;
}

.additional-info {
  margin-top: 20px;
}

.additional-details {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.additional-details h4 {
  color: var(--accent-orange);
  margin-bottom: 10px;
}

.additional-details p {
  color: var(--text-muted);
  line-height: 1.6;
}

.similar-workouts {
  margin-top: 40px;
}

.similar-workouts h3 {
  color: var(--accent-orange);
  margin-bottom: 20px;
}

.similar-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.similar-card {
  padding: 20px;
  text-align: center;
  transition: transform 0.3s ease;
}

.similar-card:hover {
  transform: translateY(-5px);
}

.similar-card h4 {
  color: var(--accent-orange);
  margin-bottom: 10px;
}

.similar-card p {
  color: var(--text-muted);
  margin: 5px 0;
  font-size: 0.9rem;
}
</style>