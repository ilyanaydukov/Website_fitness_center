<template>
  <div class="container">
    <div class="feedback-container">
      <div v-if="isLoading" class="loader"></div>
      
      <div v-else-if="error" class="error-container">
        <div class="alert alert-danger">
          {{ error }}
        </div>
        <router-link to="/trainers" class="btn btn-primary">
          Вернуться к тренерам
        </router-link>
      </div>
      
      <div v-else-if="trainer" class="feedback-form">
        <div class="feedback-header">
          <h1 class="page-title">Отзыв о тренере</h1>
          <button @click="$router.back()" class="btn btn-secondary">
            ← Назад
          </button>
        </div>
        
        <div class="trainer-info card">
          <div class="trainer-header">
            <h2>{{ trainer.first_name }} {{ trainer.last_name }}</h2>
            <span class="specialization">
              {{ trainer.specialization?.name || 'Тренер' }}
            </span>
          </div>
          
          <div class="trainer-details">
            <p v-if="trainer.work_experience">
              <strong>Опыт работы:</strong> {{ trainer.work_experience }} лет
            </p>
            <p v-if="trainer.specialization?.description">
              <strong>Специализация:</strong> {{ trainer.specialization.description }}
            </p>
          </div>
        </div>
        
        <form @submit.prevent="submitFeedback" class="card">
          <div class="form-group">
            <label class="form-label">Оценка</label>
            <div class="rating-input">
              <div 
                v-for="star in 5" 
                :key="star" 
                class="star"
                :class="{ 'active': formData.mark >= star }"
                @click="formData.mark = star"
              >
                ★
              </div>
            </div>
            <small class="form-text">Кликните по звездам, чтобы выбрать оценку</small>
          </div>
          
          <div class="form-group">
            <label for="comment" class="form-label">Комментарий</label>
            <textarea
              id="comment"
              v-model="formData.comment"
              class="form-control"
              rows="5"
              placeholder="Поделитесь своими впечатлениями о тренере..."
              maxlength="500"
            ></textarea>
            <div class="char-count">
              {{ formData.comment.length }}/500 символов
            </div>
          </div>
          
          <div v-if="submitError" class="alert alert-danger">
            {{ submitError }}
          </div>
          
          <div class="form-actions">
            <button type="submit" class="btn btn-primary btn-lg" :disabled="isSubmitting">
              {{ isSubmitting ? 'Отправка...' : 'Отправить отзыв' }}
            </button>
            <button type="button" @click="$router.back()" class="btn btn-secondary">
              Отмена
            </button>
          </div>
        </form>
        
        <div v-if="existingFeedbacks.length > 0" class="existing-feedbacks">
          <h3>Ваши предыдущие отзывы об этом тренере</h3>
          <div class="feedbacks-list">
            <div v-for="feedback in existingFeedbacks" :key="feedback.id" class="feedback-item card">
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
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { format } from 'date-fns'
import { fitnessAPI } from '../../services/api'

export default {
  name: 'FeedbackForm',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const trainer = ref(null)
    const existingFeedbacks = ref([])
    const isLoading = ref(false)
    const isSubmitting = ref(false)
    const error = ref('')
    const submitError = ref('')
    
    const formData = ref({
      mark: 5,
      comment: '',
      feedback_date: new Date().toISOString().split('T')[0]
    })
    
    const trainerId = route.params.trainerId
    
    const fetchData = async () => {
      if (!trainerId) {
        error.value = 'ID тренера не указан'
        return
      }
      
      isLoading.value = true
      try {
        const [trainerRes, feedbacksRes] = await Promise.all([
          fitnessAPI.getTrainer(trainerId),
          fitnessAPI.getTrainerFeedbacks(trainerId)
        ])
        
        trainer.value = trainerRes.data
        existingFeedbacks.value = feedbacksRes.data
        
        // Можно добавить фильтрацию только текущего пользователя
        // existingFeedbacks.value = feedbacksRes.data.filter(fb => fb.client_id === currentUser.id)
      } catch (error) {
        console.error('Error fetching data:', error)
        error.value = 'Тренер не найден'
      } finally {
        isLoading.value = false
      }
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return ''
      return format(new Date(dateString), 'dd.MM.yyyy')
    }
    
    const submitFeedback = async () => {
      if (formData.value.mark < 1 || formData.value.mark > 5) {
        submitError.value = 'Пожалуйста, поставьте оценку от 1 до 5'
        return
      }
      
      isSubmitting.value = true
      submitError.value = ''
      
      try {
        await fitnessAPI.createFeedback(trainerId, formData.value)
        alert('Отзыв успешно отправлен!')
        router.push(`/trainers/${trainerId}`)
      } catch (error) {
        submitError.value = error.response?.data?.detail || 'Ошибка отправки отзыва'
      } finally {
        isSubmitting.value = false
      }
    }
    
    onMounted(() => {
      fetchData()
    })
    
    return {
      trainer,
      existingFeedbacks,
      isLoading,
      isSubmitting,
      error,
      submitError,
      formData,
      formatDate,
      submitFeedback
    }
  }
}
</script>

<style scoped>
.feedback-container {
  max-width: 800px;
  margin: 0 auto;
}

.feedback-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.trainer-info {
  margin-bottom: 30px;
  padding: 20px;
}

.trainer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.trainer-header h2 {
  color: var(--accent-orange);
  margin: 0;
}

.specialization {
  background: linear-gradient(135deg, var(--accent-orange), var(--accent-purple));
  color: white;
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 0.9rem;
}

.trainer-details p {
  margin: 8px 0;
  color: var(--text-muted);
}

.rating-input {
  display: flex;
  gap: 10px;
  margin-bottom: 5px;
}

.star {
  font-size: 2.5rem;
  color: var(--border-color);
  cursor: pointer;
  transition: color 0.3s ease;
}

.star:hover,
.star.active {
  color: gold;
}

.char-count {
  text-align: right;
  color: var(--text-muted);
  font-size: 0.85rem;
  margin-top: 5px;
}

.form-actions {
  display: flex;
  gap: 15px;
  margin-top: 20px;
}

.existing-feedbacks {
  margin-top: 40px;
}

.existing-feedbacks h3 {
  color: var(--accent-orange);
  margin-bottom: 20px;
}

.feedbacks-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.feedback-item {
  padding: 15px;
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

.stars .star {
  font-size: 1.2rem;
  color: var(--border-color);
}

.stars .star.active {
  color: gold;
}

.rating-value {
  font-weight: 600;
  color: var(--accent-orange);
}

.feedback-date {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.feedback-comment {
  color: var(--text-muted);
  line-height: 1.5;
  font-style: italic;
}
</style>