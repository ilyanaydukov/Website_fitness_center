<template>
  <div class="container">
    <div v-if="isLoading" class="loader"></div>
    
    <div v-else-if="error" class="error-container">
      <div class="alert alert-danger">
        {{ error }}
      </div>
      <router-link to="/trainers" class="btn btn-primary">
        Вернуться к тренерам
      </router-link>
    </div>
    
    <div v-else-if="trainer" class="trainer-details">
      <div class="trainer-header">
        <h1 class="page-title">{{ trainer.first_name }} {{ trainer.last_name }}</h1>
        <button @click="$router.back()" class="btn btn-secondary">
          ← Назад
        </button>
      </div>
      
      <div class="trainer-profile card">
        <div class="profile-header">
          <div class="trainer-photo">
            <div class="photo-placeholder">{{ trainer.first_name[0] }}{{ trainer.last_name[0] }}</div>
          </div>
          <div class="profile-info">
            <div class="specialization-badge">
              {{ trainer.specialization?.name || 'Тренер' }}
            </div>
            <div class="trainer-rating" v-if="trainer.average_rating">
              <span class="stars">
                <span v-for="star in 5" :key="star" class="star" :class="{ 'active': star <= Math.round(trainer.average_rating) }">
                  ★
                </span>
              </span>
              <span class="rating-value">{{ trainer.average_rating.toFixed(1) }}/5</span>
            </div>
          </div>
        </div>
        
        <div class="profile-details">
          <div class="details-section">
            <h3>Информация о тренере</h3>
            <div class="details-grid">
              <div class="detail-item">
                <strong>Опыт работы:</strong> {{ trainer.work_experience || '0' }} лет
              </div>
              <div class="detail-item" v-if="trainer.specialization?.description">
                <strong>Специализация:</strong> {{ trainer.specialization.description }}
              </div>
              <div class="detail-item" v-if="trainer.email">
                <strong>Email:</strong> {{ trainer.email }}
              </div>
              <div class="detail-item" v-if="trainer.phone">
                <strong>Телефон:</strong> {{ trainer.phone }}
              </div>
              <div class="detail-item" v-if="trainer.education">
                <strong>Образование:</strong> {{ trainer.education }}
              </div>
              <div class="detail-item" v-if="trainer.certifications">
                <strong>Сертификаты:</strong> {{ trainer.certifications }}
              </div>
            </div>
          </div>
          
          <div class="details-section" v-if="trainer.bio">
            <h3>О тренере</h3>
            <p class="bio">{{ trainer.bio }}</p>
          </div>
          
          <div class="details-section">
            <h3>Статистика</h3>
            <div class="stats-grid">
              <div class="stat-item">
                <div class="stat-value">{{ trainer.workouts_count || 0 }}</div>
                <div class="stat-label">Проведено тренировок</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ trainer.clients_count || 0 }}</div>
                <div class="stat-label">Клиентов обучил</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ trainer.feedbacks_count || 0 }}</div>
                <div class="stat-label">Отзывов</div>
              </div>
            </div>
          </div>
          
          <div class="details-section">
            <div class="section-header">
              <h3>Расписание тренера</h3>
              <button @click="viewFullSchedule" class="btn btn-secondary">
                Все тренировки
              </button>
            </div>
            
            <div v-if="upcomingWorkouts.length === 0" class="empty-state">
              <p>Нет предстоящих тренировок</p>
            </div>
            
            <div v-else class="workouts-list">
              <div v-for="workout in upcomingWorkouts.slice(0, 5)" :key="workout.id" class="workout-item">
                <div class="workout-info">
                  <h4>{{ workout.service?.name }}</h4>
                  <p>{{ formatDate(workout.workout_date) }} {{ workout.start_time }} - {{ workout.end_time }}</p>
                  <p><small>{{ workout.room?.name }}</small></p>
                </div>
                <div class="workout-actions">
                  <button @click="viewWorkoutDetails(workout.id)" class="btn btn-sm btn-secondary">
                    Подробнее
                  </button>
                  <button 
                    v-if="isAuthenticated && !isEmployee"
                    @click="registerForWorkout(workout.id)"
                    class="btn btn-sm btn-primary"
                    :disabled="workout.current_number_of_recorded >= workout.max_persons_capacity"
                  >
                    {{ workout.current_number_of_recorded >= workout.max_persons_capacity ? 'Мест нет' : 'Записаться' }}
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <div class="details-section" v-if="feedbacks.length > 0">
            <h3>Отзывы</h3>
            <div class="feedbacks-list">
              <div v-for="feedback in feedbacks.slice(0, 3)" :key="feedback.id" class="feedback-item">
                <div class="feedback-header">
                  <div class="feedback-rating">
                    <span class="stars">
                      <span v-for="star in 5" :key="star" class="star" :class="{ 'active': star <= feedback.mark }">
                        ★
                      </span>
                    </span>
                    <span class="rating-value">{{ feedback.mark }}/5</span>
                  </div>
                  <span class="feedback-date">{{ formatDate(feedback.feedback_date) }}</span>
                </div>
                <div class="feedback-comment">
                  {{ feedback.comment || 'Без комментария' }}
                </div>
                <div class="feedback-client" v-if="feedback.client">
                  {{ feedback.client.first_name }} {{ feedback.client.last_name }}
                </div>
              </div>
            </div>
            
            <button @click="viewAllFeedbacks" class="btn btn-secondary">
              Все отзывы
            </button>
          </div>
          
          <div class="details-section actions-section">
            <button @click="viewTrainerSchedule" class="btn btn-primary">
              Посмотреть расписание
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
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { format } from 'date-fns'
import { fitnessAPI } from '../../services/api'
import { useAuthStore } from '../../store/auth'

export default {
  name: 'TrainerDetails',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const authStore = useAuthStore()
    
    const trainer = ref(null)
    const feedbacks = ref([])
    const upcomingWorkouts = ref([])
    const isLoading = ref(false)
    const error = ref('')
    
    const trainerId = route.params.id
    
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const isEmployee = computed(() => authStore.isEmployee)
    
    const fetchData = async () => {
      if (!trainerId) {
        error.value = 'ID тренера не указан'
        return
      }
      
      isLoading.value = true
      try {
        const [trainerRes, feedbacksRes, workoutsRes] = await Promise.all([
          fitnessAPI.getTrainer(trainerId),
          fitnessAPI.getTrainerFeedbacks(trainerId),
          fitnessAPI.getWorkouts({ trainer_id: trainerId, dateFrom: new Date().toISOString().split('T')[0] })
        ])
        
        trainer.value = trainerRes.data
        feedbacks.value = feedbacksRes.data
        upcomingWorkouts.value = workoutsRes.data
        
        // Считаем статистику
        trainer.value.feedbacks_count = feedbacks.value.length
        trainer.value.average_rating = feedbacks.value.length > 0 
          ? feedbacks.value.reduce((sum, fb) => sum + fb.mark, 0) / feedbacks.value.length
          : 0
          
      } catch (error) {
        console.error('Error fetching trainer details:', error)
        error.value = 'Тренер не найден'
      } finally {
        isLoading.value = false
      }
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return ''
      return format(new Date(dateString), 'dd.MM.yyyy')
    }
    
    const viewTrainerSchedule = () => {
      router.push({
        path: '/schedule',
        query: { trainerId }
      })
    }
    
    const viewFullSchedule = () => {
      viewTrainerSchedule()
    }
    
    const viewWorkoutDetails = (workoutId) => {
      router.push(`/workout/${workoutId}`)
    }
    
    const registerForWorkout = async (workoutId) => {
      try {
        await fitnessAPI.registerForWorkout(workoutId)
        alert('Вы успешно записались на тренировку!')
        fetchData()
      } catch (error) {
        alert(error.response?.data?.detail || 'Ошибка записи')
      }
    }
    
    const leaveFeedback = () => {
      router.push(`/feedback/${trainerId}`)
    }
    
    const viewAllFeedbacks = () => {
      // Можно реализовать модальное окно со всеми отзывами
      console.log('View all feedbacks for trainer:', trainerId)
    }
    
    onMounted(() => {
      fetchData()
    })
    
    return {
      trainer,
      feedbacks,
      upcomingWorkouts,
      isLoading,
      error,
      isAuthenticated,
      isEmployee,
      formatDate,
      viewTrainerSchedule,
      viewFullSchedule,
      viewWorkoutDetails,
      registerForWorkout,
      leaveFeedback,
      viewAllFeedbacks
    }
  }
}
</script>

<style scoped>
.trainer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.trainer-profile {
  padding: 30px;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 30px;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border-color);
}

.trainer-photo {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent-orange), var(--accent-purple));
  display: flex;
  align-items: center;
  justify-content: center;
}

.photo-placeholder {
  font-size: 3rem;
  font-weight: bold;
  color: white;
}

.profile-info {
  flex: 1;
}

.specialization-badge {
  display: inline-block;
  background: linear-gradient(135deg, var(--accent-orange), var(--accent-purple));
  color: white;
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 15px;
}

.trainer-rating {
  display: flex;
  align-items: center;
  gap: 10px;
}

.stars .star {
  font-size: 1.5rem;
  color: var(--border-color);
}

.stars .star.active {
  color: gold;
}

.rating-value {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--accent-orange);
}

.details-section {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border-color);
}

.details-section:last-child {
  border-bottom: none;
}

.details-section h3 {
  color: var(--accent-orange);
  margin-bottom: 20px;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
}

.detail-item {
  padding: 10px;
  background-color: var(--primary-dark);
  border-radius: var(--radius);
}

.detail-item strong {
  color: var(--accent-orange);
  margin-right: 10px;
}

.bio {
  color: var(--text-muted);
  line-height: 1.6;
  font-size: 1.1rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 20px;
}

.stat-item {
  text-align: center;
  padding: 20px;
  background-color: var(--primary-dark);
  border-radius: var(--radius);
}

.stat-value {
  display: block;
  font-size: 2.5rem;
  font-weight: bold;
  color: var(--accent-orange);
  margin-bottom: 10px;
}

.stat-label {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.workouts-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.workout-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: var(--primary-dark);
  border-radius: var(--radius);
}

.workout-info h4 {
  color: var(--accent-orange);
  margin-bottom: 5px;
}

.workout-info p {
  color: var(--text-muted);
  margin: 2px 0;
}

.workout-actions {
  display: flex;
  gap: 10px;
}

.feedbacks-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 20px;
}

.feedback-item {
  padding: 15px;
  background-color: var(--primary-dark);
  border-radius: var(--radius);
}

.feedback-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.feedback-rating {
  display: flex;
  align-items: center;
  gap: 10px;
}

.feedback-date {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.feedback-comment {
  color: var(--text-muted);
  line-height: 1.5;
  margin-bottom: 10px;
  font-style: italic;
}

.feedback-client {
  color: var(--text-light);
  font-size: 0.9rem;
  font-weight: 500;
}

.actions-section {
  display: flex;
  gap: 15px;
  justify-content: center;
  padding-top: 20px;
}
</style>